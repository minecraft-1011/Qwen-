"""
Risk Management Module for FundingPips Trading System

CRITICAL: This module enforces FundingPips rules and protects capital.
Risk management operates INDEPENDENTLY from strategy logic and can override any signal.
"""

from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional, Dict, List
import pandas as pd
import numpy as np


@dataclass
class RiskLimits:
    """Risk limit parameters"""
    
    # FundingPips rules
    max_daily_loss_percent: float = 5.0
    max_total_loss_percent: float = 10.0
    profit_target_percent: float = 8.0
    
    # Safety buffers (operate below actual limits)
    daily_loss_buffer: float = 1.0
    total_loss_buffer: float = 1.0
    
    # Position limits
    max_positions: int = 3
    max_leverage: float = 10.0
    risk_per_trade: float = 0.005  # 0.5%
    
    # Correlation limits
    max_correlation_exposure: float = 2.0
    
    @property
    def effective_daily_limit(self) -> float:
        return self.max_daily_loss_percent - self.daily_loss_buffer
    
    @property
    def effective_total_limit(self) -> float:
        return self.max_total_loss_percent - self.total_loss_buffer


@dataclass
class RiskStatus:
    """Current risk status"""
    
    daily_pnl_percent: float
    total_pnl_percent: float
    current_drawdown: float
    max_drawdown: float
    open_positions: int
    exposure: float
    trading_allowed: bool
    reason_blocked: Optional[str] = None


class RiskManager:
    """
    Risk Manager with FundingPips Rules Enforcement
    
    Features:
    - Daily loss limit monitoring (5% max, 4% soft limit)
    - Total loss limit monitoring (10% max, 9% soft limit)
    - Position sizing based on volatility and risk
    - Correlation limits
    - News filter integration
    - Emergency shutdown capability
    """
    
    def __init__(self, config: RiskLimits = None):
        self.config = config or RiskLimits()
        
        # State tracking
        self.starting_balance = 10000.0
        self.current_balance = self.starting_balance
        self.peak_balance = self.starting_balance
        self.daily_start_balance = self.starting_balance
        
        # Trade tracking
        self.trades_today = []
        self.total_trades = []
        self.open_positions = []
        
        # Daily tracking
        self.last_reset_date = None
        
        # Emergency shutdown flag
        self.emergency_shutdown = False
        self.shutdown_reason = None
        
        # Minimum trading days tracking (FundingPips requirement)
        self.trading_days_with_trades = set()
    
    def update_balance(self, new_balance: float, trade_date: datetime):
        """Update balance and track drawdowns"""
        
        # Reset daily tracking if new day
        today = trade_date.date()
        if self.last_reset_date != today:
            self.daily_start_balance = self.current_balance
            self.trades_today = []
            self.last_reset_date = today
        
        # Update balances
        prev_balance = self.current_balance
        self.current_balance = new_balance
        
        # Update peak balance
        if new_balance > self.peak_balance:
            self.peak_balance = new_balance
        
        # Track trade P&L
        if len(self.total_trades) > 0:
            pnl = new_balance - prev_balance
            self.trades_today.append({
                'date': trade_date,
                'pnl': pnl,
                'balance': new_balance
            })
            self.total_trades.append({
                'date': trade_date,
                'pnl': pnl,
                'balance': new_balance
            })
    
    def check_risk_limits(self) -> RiskStatus:
        """Check all risk limits and return status"""
        
        if self.emergency_shutdown:
            return RiskStatus(
                daily_pnl_percent=self.get_daily_pnl_percent(),
                total_pnl_percent=self.get_total_pnl_percent(),
                current_drawdown=self.get_current_drawdown(),
                max_drawdown=self.get_max_drawdown(),
                open_positions=len(self.open_positions),
                exposure=self.get_total_exposure(),
                trading_allowed=False,
                reason_blocked=f"Emergency shutdown: {self.shutdown_reason}"
            )
        
        # Calculate metrics
        daily_pnl = self.get_daily_pnl_percent()
        total_pnl = self.get_total_pnl_percent()
        current_dd = self.get_current_drawdown()
        max_dd = self.get_max_drawdown()
        
        # Check daily loss limit
        if daily_pnl <= -self.config.effective_daily_limit:
            return RiskStatus(
                daily_pnl_percent=daily_pnl,
                total_pnl_percent=total_pnl,
                current_drawdown=current_dd,
                max_drawdown=max_dd,
                open_positions=len(self.open_positions),
                exposure=self.get_total_exposure(),
                trading_allowed=False,
                reason_blocked=f"Daily loss limit reached: {daily_pnl:.2f}%"
            )
        
        # Check total loss limit
        if total_pnl <= -self.config.effective_total_limit:
            return RiskStatus(
                daily_pnl_percent=daily_pnl,
                total_pnl_percent=total_pnl,
                current_drawdown=current_dd,
                max_drawdown=max_dd,
                open_positions=len(self.open_positions),
                exposure=self.get_total_exposure(),
                trading_allowed=False,
                reason_blocked=f"Total loss limit reached: {total_pnl:.2f}%"
            )
        
        # Check profit target (for evaluation phases)
        if total_pnl >= self.config.profit_target_percent:
            return RiskStatus(
                daily_pnl_percent=daily_pnl,
                total_pnl_percent=total_pnl,
                current_drawdown=current_dd,
                max_drawdown=max_dd,
                open_positions=len(self.open_positions),
                exposure=self.get_total_exposure(),
                trading_allowed=False,
                reason_blocked=f"Profit target reached: {total_pnl:.2f}%"
            )
        
        # Check position limits
        if len(self.open_positions) >= self.config.max_positions:
            return RiskStatus(
                daily_pnl_percent=daily_pnl,
                total_pnl_percent=total_pnl,
                current_drawdown=current_dd,
                max_drawdown=max_dd,
                open_positions=len(self.open_positions),
                exposure=self.get_total_exposure(),
                trading_allowed=False,
                reason_blocked=f"Maximum positions reached: {len(self.open_positions)}"
            )
        
        # All checks passed
        return RiskStatus(
            daily_pnl_percent=daily_pnl,
            total_pnl_percent=total_pnl,
            current_drawdown=current_dd,
            max_drawdown=max_dd,
            open_positions=len(self.open_positions),
            exposure=self.get_total_exposure(),
            trading_allowed=True
        )
    
    def get_daily_pnl_percent(self) -> float:
        """Calculate daily P&L percentage"""
        return ((self.current_balance - self.daily_start_balance) / self.daily_start_balance) * 100
    
    def get_total_pnl_percent(self) -> float:
        """Calculate total P&L percentage from start"""
        return ((self.current_balance - self.starting_balance) / self.starting_balance) * 100
    
    def get_current_drawdown(self) -> float:
        """Calculate current drawdown from peak"""
        if self.peak_balance == 0:
            return 0.0
        return ((self.peak_balance - self.current_balance) / self.peak_balance) * 100
    
    def get_max_drawdown(self) -> float:
        """Calculate maximum historical drawdown"""
        if len(self.total_trades) < 2:
            return self.get_current_drawdown()
        
        # Calculate running maximum
        balances = [t['balance'] for t in self.total_trades]
        running_max = pd.Series(balances).cummax()
        drawdowns = (running_max - pd.Series(balances)) / running_max * 100
        
        return max(drawdowns.max(), self.get_current_drawdown())
    
    def get_total_exposure(self) -> float:
        """Calculate total portfolio exposure"""
        if not self.open_positions:
            return 0.0
        
        return sum(pos.get('notional', 0) for pos in self.open_positions)
    
    def calculate_position_size(
        self,
        instrument: str,
        entry_price: float,
        stop_loss: float,
        account_balance: float = None
    ) -> float:
        """
        Calculate position size based on risk parameters
        
        Returns:
            Position size in lots/units
        """
        
        balance = account_balance or self.current_balance
        risk_amount = balance * self.config.risk_per_trade
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit == 0:
            return 0.0
        
        # Calculate position size
        position_size = risk_amount / risk_per_unit
        
        # Apply leverage limit
        max_notional = balance * self.config.max_leverage
        max_position = max_notional / entry_price
        
        position_size = min(position_size, max_position)
        
        return position_size
    
    def validate_signal(self, signal, current_status: RiskStatus) -> tuple:
        """
        Validate a trading signal against risk limits
        
        Returns:
            (is_valid, modified_signal_or_none, reason)
        """
        
        if not current_status.trading_allowed:
            return False, None, current_status.reason_blocked
        
        # Check if signal direction is allowed
        if signal.direction != 0:
            # Would this exceed position limits?
            if len(self.open_positions) >= self.config.max_positions:
                return False, None, "Position limit would be exceeded"
            
            # Check correlation exposure
            # (Simplified - in production would check correlation matrix)
            current_exposure = self.get_total_exposure()
            if current_exposure >= self.config.max_correlation_exposure * self.current_balance:
                return False, None, "Correlation exposure limit reached"
        
        return True, signal, "Approved"
    
    def add_position(self, position_info: dict):
        """Add an open position to tracking"""
        self.open_positions.append(position_info)
        
        # Track trading day
        trade_date = position_info.get('date', datetime.now()).date()
        self.trading_days_with_trades.add(trade_date)
    
    def remove_position(self, position_id: str):
        """Remove a closed position from tracking"""
        self.open_positions = [p for p in self.open_positions if p.get('id') != position_id]
    
    def emergency_stop(self, reason: str):
        """Trigger emergency shutdown"""
        self.emergency_shutdown = True
        self.shutdown_reason = reason
    
    def reset_emergency_stop(self):
        """Reset emergency shutdown (requires manual intervention)"""
        self.emergency_shutdown = False
        self.shutdown_reason = None
    
    def get_minimum_days_status(self) -> dict:
        """Check minimum trading days requirement"""
        days_with_trades = len(self.trading_days_with_trades)
        days_required = 5  # FundingPips requirement
        
        return {
            'days_with_trades': days_with_trades,
            'days_required': days_required,
            'requirement_met': days_with_trades >= days_required,
            'remaining_days': max(0, days_required - days_with_trades)
        }
    
    def generate_risk_report(self) -> dict:
        """Generate comprehensive risk report"""
        
        status = self.check_risk_limits()
        min_days = self.get_minimum_days_status()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'account': {
                'starting_balance': self.starting_balance,
                'current_balance': self.current_balance,
                'peak_balance': self.peak_balance,
            },
            'performance': {
                'daily_pnl_percent': status.daily_pnl_percent,
                'total_pnl_percent': status.total_pnl_percent,
                'current_drawdown': status.current_drawdown,
                'max_drawdown': status.max_drawdown,
            },
            'limits': {
                'daily_limit': f"-{self.config.effective_daily_limit}%",
                'total_limit': f"-{self.config.effective_total_limit}%",
                'profit_target': f"{self.config.profit_target_percent}%",
            },
            'positions': {
                'open_count': len(self.open_positions),
                'max_allowed': self.config.max_positions,
                'total_exposure': self.get_total_exposure(),
            },
            'requirements': min_days,
            'status': {
                'trading_allowed': status.trading_allowed,
                'reason_blocked': status.reason_blocked,
                'emergency_shutdown': self.emergency_shutdown,
            },
            'trade_counts': {
                'trades_today': len(self.trades_today),
                'total_trades': len(self.total_trades),
            }
        }


def create_risk_manager(config_dict: dict = None) -> RiskManager:
    """Factory function to create risk manager"""
    
    if config_dict:
        config = RiskLimits(**config_dict)
    else:
        config = RiskLimits()
    
    return RiskManager(config)
