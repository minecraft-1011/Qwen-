# FundingPips Trading System

A professional algorithmic trading system designed specifically for **FundingPips** prop firm evaluation and funded accounts, trading Forex majors and Gold (XAU/USD).

## ⚠️ CRITICAL SAFETY WARNINGS

- **TRADING_MODE defaults to PAPER** - Never switch to LIVE without explicit confirmation
- **NEVER commit .env file** - Contains sensitive API credentials
- **Prop firm rules are hardcoded** - System enforces 5% daily / 10% total loss limits
- **Emergency kill switch built-in** - Automatic shutdown if limits approached

## System Overview

This system is optimized for:
- **Instruments**: EUR/USD, GBP/USD, XAU/USD (Gold)
- **Strategy**: Trend Following with Volatility Overlay
- **Timeframe**: Daily signals with 4-hour entries
- **Account Type**: FundingPips evaluation and funded accounts

## FundingPips Rules Integration

The system enforces these rules automatically:

| Rule | FundingPips Limit | System Safety Limit |
|------|------------------|---------------------|
| Max Daily Loss | 5% | 4% (1% buffer) |
| Max Total Loss | 10% | 9% (1% buffer) |
| Profit Target (Phase 1) | 8% | Configurable |
| Profit Target (Phase 2) | 5% | Configurable |
| Minimum Trading Days | 5 | Enforced |
| Leverage | Up to 1:100 | Limited to 1:10 |

## Project Structure

```
fundingpips_trading_system/
├── config/                  # Configuration files
│   └── .env.example        # Template (safe to commit)
├── data/                    # Data storage
│   ├── raw/                # Raw market data
│   ├── processed/          # Cleaned data
│   └── features/           # Engineered features
├── src/                     # Source code
│   ├── data/               # Data loaders and cleaners
│   ├── features/           # Feature engineering
│   ├── strategies/         # Trading strategies
│   ├── backtesting/        # Backtesting engine
│   ├── risk/               # Risk management
│   ├── live/               # Live/paper trading
│   └── utils/              # Utilities
├── tests/                   # Unit and integration tests
├── notebooks/               # Jupyter research notebooks
├── reports/                 # Performance reports
├── logs/                    # System logs
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Quick Start

### 1. Clone and Setup

```bash
cd fundingpips_trading_system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example .env
# Edit .env with your settings (NEVER commit this file)
```

### 3. Download Data

```bash
# Download historical data from Dukascopy
python src/data/download_data.py
```

### 4. Run Backtest

```bash
python src/backtesting/run_backtest.py
```

### 5. Paper Trade

```bash
python src/live/paper_trading.py
```

## Strategy Details

### Trend Following with Volatility Overlay

**Entry Conditions:**
- Fast MA crosses above Slow MA (long) or below (short)
- ATR-based volatility filter (avoid extremely low vol)
- No high-impact news within 2 hours

**Exit Conditions:**
- Price crosses below/above exit MA
- Stop loss hit (ATR-based)
- Time-based exit (optional)

**Position Sizing:**
- Risk per trade: 0.5% of account (configurable)
- Volatility-targeted: Position size inversely proportional to ATR
- Maximum 3 concurrent positions
- Correlation limits enforced

## Risk Management

### Multi-Layer Protection

1. **Trade Level**
   - Stop loss on every trade
   - Maximum risk per trade: 0.5%
   
2. **Daily Level**
   - Hard stop at 4% daily loss
   - Trading halt for the day
   
3. **Account Level**
   - Hard stop at 9% total loss
   - System shutdown, manual review required
   
4. **System Level**
   - News filter avoids high-impact events
   - Weekend position reduction option
   - Emergency kill switch

## Backtesting Methodology

### Anti-Overfitting Measures

- Walk-forward analysis (minimum 4 windows)
- Out-of-sample testing (20% holdout)
- Parameter sensitivity analysis (±20%)
- Transaction cost stress testing (2x spreads)
- Multiple regime testing (bull/bear/sideways)

### Realistic Assumptions

- Spread: 0.8 pips (EUR/USD), 1.2 pips (GBP/USD), 20 cents (Gold)
- Slippage: 0.5 pips average
- Commission: $0 (most forex brokers)
- Partial fills: Modeled for large orders
- Gaps: Overnight and weekend gaps included

## Data Sources

### Historical Data (Free)
- **Dukascopy**: High-quality tick data, converted to OHLCV
- Download script included in `src/data/`

### Real-Time Data (Paper/Live)
- **OANDA API**: Free with demo account
- **Interactive Brokers**: Free with funded account
- **Broker Direct**: MT4/MT5 bridge (if available)

## Testing & Validation

### Strategy Acceptance Criteria

A strategy must pass ALL tests:

- ✅ In-sample Sharpe > 0.7
- ✅ Out-of-sample Sharpe > 0.4
- ✅ 60%+ profitable walk-forward windows
- ✅ Profitable at 2x transaction costs
- ✅ Maximum drawdown < 20%
- ✅ Works in multiple market regimes
- ✅ Parameter stability (< 30% variation)

## Development Phases

### Phase 1: Research Framework ✅
- Data download and cleaning
- Feature engineering
- Basic backtesting
- Strategy research tools

### Phase 2: Advanced Backtesting 🔄
- Event-driven engine
- Realistic execution modeling
- Walk-forward analysis
- Robustness testing

### Phase 3: Paper Trading ⏳
- Real-time data integration
- Order simulation
- Performance tracking
- Minimum 50 trades / 3 months

### Phase 4: Live Trading 🔒
- Broker API integration
- Production monitoring
- **REQUIRES EXPLICIT APPROVAL**

## Security

### Credential Management

- All secrets in `.env` file (never committed)
- API keys rotated regularly
- Encrypted storage for sensitive data
- Audit logging enabled

### Safety Features

- Trading mode defaults to PAPER
- Live mode requires explicit configuration
- Emergency kill switch always available
- Daily reconciliation checks

## Monitoring & Reporting

### Key Metrics Tracked

- Daily P&L
- Drawdown (daily and total)
- Win rate, profit factor
- Sharpe ratio, Sortino ratio
- Exposure by instrument
- Correlation matrix

### Alerts

- Daily loss limit approached (>3%)
- Total loss limit approached (>8%)
- Position limit reached
- Connection issues
- Stale data detection

## Common Mistakes Avoided

This system specifically prevents:

- ❌ Over-leveraging (capped at 1:10)
- ❌ Revenge trading (daily loss limits)
- ❌ Martingale strategies (fixed risk per trade)
- ❌ News gambling (automatic filter)
- ❌ Weekend gap risk (reduction option)
- ❌ Overfitting (rigorous validation)
- ❌ Look-ahead bias (point-in-time data)
- ❌ Survivorship bias (all data included)

## Contributing

1. Create feature branch
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Document any new parameters
5. Submit pull request

## License

This project is for personal use only. Not for commercial redistribution.

## Disclaimer

**Trading involves substantial risk of loss and is not suitable for all investors.**

This system is provided for educational purposes only. Past performance does not guarantee future results. Always test thoroughly with paper trading before risking real capital.

The authors are not responsible for any financial losses incurred through use of this software.

---

**Current Status**: Phase 1 Implementation Ready
**Next Step**: Install dependencies and download data

For questions or issues, check the documentation in `/docs` or run the test suite.
