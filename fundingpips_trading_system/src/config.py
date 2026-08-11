"""
Configuration Management for FundingPips Trading System

This module handles all configuration loading and validation.
Uses Pydantic for type safety and validation.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv


class FundingPipsConfig(BaseModel):
    """FundingPips account rules and limits"""
    
    account_size: float = Field(default=10000.0, ge=1000, le=200000)
    evaluation_phase: str = Field(default="phase1")
    profit_target_percent: float = Field(default=8.0, ge=1.0, le=20.0)
    max_daily_loss_percent: float = Field(default=5.0)
    max_total_loss_percent: float = Field(default=10.0)
    min_trading_days: int = Field(default=5, ge=1)
    
    # Safety buffers (operate below actual limits)
    daily_loss_buffer_percent: float = Field(default=1.0)
    total_loss_buffer_percent: float = Field(default=1.0)
    
    @property
    def effective_daily_loss_limit(self) -> float:
        """Daily loss limit with safety buffer applied"""
        return self.max_daily_loss_percent - self.daily_loss_buffer_percent
    
    @property
    def effective_total_loss_limit(self) -> float:
        """Total loss limit with safety buffer applied"""
        return self.max_total_loss_percent - self.total_loss_buffer_percent
    
    @field_validator('evaluation_phase')
    @classmethod
    def validate_phase(cls, v: str) -> str:
        allowed = ['phase1', 'phase2', 'funded']
        if v not in allowed:
            raise ValueError(f'evaluation_phase must be one of {allowed}')
        return v


class RiskConfig(BaseModel):
    """Risk management parameters"""
    
    risk_per_trade_percent: float = Field(default=0.5, ge=0.1, le=2.0)
    max_leverage: int = Field(default=10, ge=1, le=30)
    max_open_positions: int = Field(default=3, ge=1, le=10)
    max_correlation_exposure: float = Field(default=2.0, ge=1.0, le=5.0)
    enable_news_filter: bool = Field(default=True)
    weekend_position_reduction: bool = Field(default=True)


class InstrumentConfig(BaseModel):
    """Instrument-specific settings"""
    
    instruments: List[str] = Field(default=["EUR/USD", "GBP/USD", "XAU/USD"])
    spread_eurusd: float = Field(default=0.8, ge=0.1)
    spread_gbpusd: float = Field(default=1.2, ge=0.1)
    spread_xauusd: float = Field(default=20.0, ge=1.0)  # In cents
    commission_per_lot: float = Field(default=0.0, ge=0.0)
    slippage_pips: float = Field(default=0.5, ge=0.0)
    
    def get_spread(self, instrument: str) -> float:
        """Get spread for specific instrument"""
        spreads = {
            'EUR/USD': self.spread_eurusd,
            'GBP/USD': self.spread_gbpusd,
            'XAU/USD': self.spread_xauusd,
        }
        return spreads.get(instrument, 1.0)


class StrategyConfig(BaseModel):
    """Trading strategy parameters"""
    
    strategy_type: str = Field(default="trend_following")
    trend_fast_period: int = Field(default=20, ge=5, le=50)
    trend_slow_period: int = Field(default=50, ge=20, le=200)
    trend_exit_period: int = Field(default=10, ge=5, le=50)
    atr_period: int = Field(default=14, ge=7, le=28)
    volatility_target_percent: float = Field(default=1.0, ge=0.5, le=5.0)
    timeframe: str = Field(default="D1")
    entry_timeframe: str = Field(default="H4")
    
    @field_validator('timeframe', 'entry_timeframe')
    @classmethod
    def validate_timeframe(cls, v: str) -> str:
        allowed = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN']
        if v not in allowed:
            raise ValueError(f'timeframe must be one of {allowed}')
        return v


class DataConfig(BaseModel):
    """Data handling configuration"""
    
    data_source: str = Field(default="dukascopy")
    data_dir: Path = Field(default=Path("data"))
    cache_dir: Path = Field(default=Path(".cache"))
    
    @field_validator('data_dir', 'cache_dir')
    @classmethod
    def validate_paths(cls, v: Path) -> Path:
        # Ensure paths are absolute relative to project root
        if not v.is_absolute():
            project_root = Path(__file__).parent.parent
            v = project_root / v
        return v


class BacktestConfig(BaseModel):
    """Backtesting parameters"""
    
    initial_capital: float = Field(default=10000.0, ge=1000.0)
    commission_rate: float = Field(default=0.0, ge=0.0, le=0.01)
    slippage_percent: float = Field(default=0.0005, ge=0.0, le=0.01)


class LoggingConfig(BaseModel):
    """Logging configuration"""
    
    log_level: str = Field(default="INFO")
    log_file: Path = Field(default=Path("logs/trading_system.log"))
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed:
            raise ValueError(f'log_level must be one of {allowed}')
        return v.upper()


class TradingSystemConfig(BaseModel):
    """Master configuration containing all subsystems"""
    
    trading_mode: str = Field(default="paper")
    funding_pips: FundingPipsConfig = Field(default_factory=FundingPipsConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    instrument: InstrumentConfig = Field(default_factory=InstrumentConfig)
    strategy: StrategyConfig = Field(default_factory=StrategyConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    backtest: BacktestConfig = Field(default_factory=BacktestConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    @field_validator('trading_mode')
    @classmethod
    def validate_trading_mode(cls, v: str) -> str:
        allowed = ['backtest', 'paper', 'live']
        if v not in allowed:
            raise ValueError(f'trading_mode must be one of {allowed}')
        # Safety check: never default to live
        if v == 'live':
            import warnings
            warnings.warn(
                "LIVE TRADING MODE ACTIVATED - Ensure all safety checks are complete",
                UserWarning,
                stacklevel=2
            )
        return v
    
    @classmethod
    def load_from_env(cls, env_file: Optional[Path] = None) -> 'TradingSystemConfig':
        """Load configuration from environment variables"""
        
        # Determine .env file location
        if env_file is None:
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"
        
        # Load environment variables
        if env_file.exists():
            load_dotenv(env_file)
        else:
            import warnings
            warnings.warn(f".env file not found at {env_file}, using defaults")
        
        # Map environment variables to config structure
        config_dict = {
            'trading_mode': os.getenv('TRADING_MODE', 'paper'),
            'funding_pips': {
                'account_size': float(os.getenv('ACCOUNT_SIZE', '10000')),
                'evaluation_phase': os.getenv('EVALUATION_PHASE', 'phase1'),
                'profit_target_percent': float(os.getenv('PROFIT_TARGET_PERCENT', '8.0')),
                'max_daily_loss_percent': float(os.getenv('MAX_DAILY_LOSS_PERCENT', '5.0')),
                'max_total_loss_percent': float(os.getenv('MAX_TOTAL_LOSS_PERCENT', '10.0')),
                'min_trading_days': int(os.getenv('MIN_TRADING_DAYS', '5')),
                'daily_loss_buffer_percent': float(os.getenv('DAILY_LOSS_BUFFER_PERCENT', '1.0')),
                'total_loss_buffer_percent': float(os.getenv('TOTAL_LOSS_BUFFER_PERCENT', '1.0')),
            },
            'risk': {
                'risk_per_trade_percent': float(os.getenv('RISK_PER_TRADE_PERCENT', '0.5')),
                'max_leverage': int(os.getenv('MAX_LEVERAGE', '10')),
                'max_open_positions': int(os.getenv('MAX_OPEN_POSITIONS', '3')),
                'max_correlation_exposure': float(os.getenv('MAX_CORRELATION_EXPOSURE', '2.0')),
                'enable_news_filter': os.getenv('ENABLE_NEWS_FILTER', 'true').lower() == 'true',
                'weekend_position_reduction': os.getenv('WEEKEND_POSITION_REDUCTION', 'true').lower() == 'true',
            },
            'instrument': {
                'instruments': [x.strip() for x in os.getenv('INSTRUMENTS', 'EUR/USD,GBP/USD,XAU/USD').split(',')],
                'spread_eurusd': float(os.getenv('SPREAD_EURUSD', '0.8')),
                'spread_gbpusd': float(os.getenv('SPREAD_GBPUSD', '1.2')),
                'spread_xauusd': float(os.getenv('SPREAD_XAUUSD', '20.0')),
                'commission_per_lot': float(os.getenv('COMMISSION_PER_LOT', '0.0')),
                'slippage_pips': float(os.getenv('SLIPPAGE_PIPS', '0.5')),
            },
            'strategy': {
                'strategy_type': os.getenv('STRATEGY_TYPE', 'trend_following'),
                'trend_fast_period': int(os.getenv('TREND_FAST_PERIOD', '20')),
                'trend_slow_period': int(os.getenv('TREND_SLOW_PERIOD', '50')),
                'trend_exit_period': int(os.getenv('TREND_EXIT_PERIOD', '10')),
                'atr_period': int(os.getenv('ATR_PERIOD', '14')),
                'volatility_target_percent': float(os.getenv('VOLATILITY_TARGET_PERCENT', '1.0')),
                'timeframe': os.getenv('TIMEFRAME', 'D1'),
                'entry_timeframe': os.getenv('ENTRY_TIMEFRAME', 'H4'),
            },
            'data': {
                'data_source': os.getenv('DATA_SOURCE', 'dukascopy'),
            },
            'backtest': {
                'initial_capital': float(os.getenv('BACKTEST_INITIAL_CAPITAL', '10000')),
                'commission_rate': float(os.getenv('BACKTEST_COMMISSION_RATE', '0.0')),
                'slippage_percent': float(os.getenv('BACKTEST_SLIPPAGE_PERCENT', '0.0005')),
            },
            'logging': {
                'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            },
        }
        
        return cls(**config_dict)


# Global configuration instance (lazy loaded)
_config: Optional[TradingSystemConfig] = None


def get_config() -> TradingSystemConfig:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = TradingSystemConfig.load_from_env()
    return _config


def reload_config() -> TradingSystemConfig:
    """Force reload configuration from environment"""
    global _config
    _config = TradingSystemConfig.load_from_env()
    return _config
