# Deep Research & Critical Review Report (Revised for Forex & Gold)

## Executive Summary
This report is **specifically tailored** to Forex and Gold trading. It challenges assumptions, evaluates strategy families for these specific markets, investigates overfitting mechanisms deeply, and re-evaluates the technology stack for practicality. The goal is to build a **minimal, robust research system** focused exclusively on currency pairs and precious metals before considering any expansion.

---

## 1. Asset Class Deep Dive: Forex & Gold Only

### Why Forex & Gold?

**Advantages:**
- ✅ **24/5 Market**: No overnight gaps (Friday close to Monday open excepted)
- ✅ **High Liquidity**: Major pairs have tight spreads
- ✅ **No PDT Rule**: No $25k minimum for day trading
- ✅ **Low Capital Requirements**: Can start with $100-500
- ✅ **Simple Data Structure**: No corporate actions, dividends, or splits
- ✅ **High Leverage Available**: 30:1 to 500:1 depending on jurisdiction
- ✅ **Gold as Inflation Hedge**: XAU/USD provides diversification
- ✅ **Prop Firm Friendly**: Many forex-focused prop firms available
- ✅ **Low Transaction Costs**: Spreads often <1 pip on majors

**Disadvantages:**
- ⚠️ **OTC Market**: No central exchange, broker-dependent pricing
- ⚠️ **Broker Risk**: Poor execution, requotes, stop hunts with bad brokers
- ⚠️ **Lower Volatility**: Majors move less than stocks/crypto (requires leverage)
- ⚠️ **Interest Rate Sensitivity**: Carry costs/benefits affect longer-term positions
- ⚠️ **Data Quality Varies**: Tick data expensive, historical quality depends on provider
- ⚠️ **Weekend Gaps**: Friday close to Monday open can gap significantly

### Recommended Instruments

**Tier 1 (Primary Focus):**
| Symbol | Name | Typical Spread | Avg Daily Range | Best For |
|--------|------|----------------|-----------------|----------|
| **EUR/USD** | Euro/US Dollar | 0.1-0.6 pips | 70-100 pips | Trend following, mean reversion |
| **GBP/USD** | British Pound/US Dollar | 0.6-1.2 pips | 100-150 pips | Breakout, trend following |
| **XAU/USD** | Gold/US Dollar | 10-30 cents | 1500-3000 cents | Trend, breakout, volatility |

**Tier 2 (Secondary - Future Expansion):**
| Symbol | Name | Typical Spread | Avg Daily Range | Notes |
|--------|------|----------------|-----------------|-------|
| **AUD/USD** | Australian Dollar/US Dollar | 0.6-1.0 pips | 60-90 pips | Commodity-linked |
| **USD/CAD** | US Dollar/Canadian Dollar | 0.8-1.2 pips | 60-80 pips | Oil-sensitive |
| **NZD/USD** | New Zealand Dollar/US Dollar | 0.8-1.2 pips | 60-80 pips | Lower liquidity |
| **XAG/USD** | Silver/US Dollar | 2-5 cents | 30-60 cents | Higher volatility than gold |

**Avoid Initially:**
- ❌ Exotic pairs (high spreads, low liquidity)
- ❌ EUR/GBP, EUR/CHF (too tight ranges)
- ❌ Cryptocurrency CFDs (unless specifically requested later)

### Market Structure Understanding

**Forex Market Hours (24/5):**
```
Sydney:   22:00 - 07:00 GMT
Tokyo:    00:00 - 09:00 GMT
London:   07:00 - 16:00 GMT
New York: 12:00 - 21:00 GMT

Overlap periods (highest liquidity):
- London/New York: 12:00-16:00 GMT (BEST for trading)
- Tokyo/London: 07:00-09:00 GMT (moderate)
```

**Gold Specifics:**
- Trades nearly 24/5 (brief daily maintenance window ~5pm ET)
- Most active during London/NY overlap
- Sensitive to: USD strength, real interest rates, inflation expectations, geopolitical risk
- Average daily range: $15-30 (1500-3000 cents)
- Spot trading allows fractional positions (unlike futures contracts)

### Broker Selection Criteria (CRITICAL)

**Must-Have Features:**
- ✅ Regulatory oversight (FCA, ASIC, NFA, CySEC)
- ✅ Segregated client funds
- ✅ Negative balance protection
- ✅ Transparent spread/commission structure
- ✅ API access (MT4/MT5, cTrader, or REST API)
- ✅ Paper trading account available
- ✅ Historical data access
- ✅ No restrictions on algorithmic trading

**Recommended Brokers for Algo Trading:**
| Broker | Regulation | Min Deposit | Spread (EUR/USD) | API | Paper Trading | Verdict |
|--------|------------|-------------|------------------|-----|---------------|---------|
| **Interactive Brokers** | Multiple | $0 | 0.1-0.2 + comm | Excellent | Yes | ✅ Best overall |
| **OANDA** | FCA, ASIC, NFA | $0 | 0.6-1.0 | Good | Yes | ✅ Great for beginners |
| **FXCM** | FCA, ASIC | $50 | 0.4-0.8 | Good | Yes | ✅ Solid choice |
| **Pepperstone** | FCA, ASIC | $200 | 0.0-0.6 (RAW) | MT4/MT5/cTrader | Yes | ✅ Low cost |
| **IC Markets** | ASIC, CySEC | $200 | 0.0-0.6 (RAW) | MT4/MT5/cTrader | Yes | ✅ Low cost |

**Avoid:**
- ❌ Unregulated offshore brokers
- ❌ Brokers promising "guaranteed profits"
- ❌ Brokers with no API access
- ❌ Brokers with history of manipulation

### Revised Recommendation: **Focus on EUR/USD, GBP/USD, and XAU/USD**

**Reasoning:**
1. **EUR/USD**: Most liquid pair, tightest spreads, excellent for trend following
2. **GBP/USD**: Higher volatility, good for breakouts and momentum
3. **XAU/USD**: Diversification, strong trending behavior, inflation hedge

**Capital Requirements:**
- **Minimum viable**: $500-1,000 (micro lots, careful risk management)
- **Comfortable**: $2,000-5,000 (standard lots possible, better risk distribution)
- **Ideal**: $10,000+ (proper position sizing, multiple strategies)

**Leverage Guidance:**
- Conservative: 5:1 to 10:1 (RECOMMENDED for beginners)
- Moderate: 10:1 to 30:1
- Aggressive: 30:1 to 50:1 (NOT recommended)
- Avoid: 100:1+ (extremely high risk of ruin)

---

## 2. Strategy Families: Forex & Gold Specific Analysis

### Strategy Evaluation for Currency Markets

| Strategy | Evidence Level | Edge Source | Timeframe | Turnover | Cost Sensitivity | Works In | Fails In | Complexity | Overfit Risk | Scalability | Verdict for Forex/Gold |
|----------|---------------|-------------|-----------|----------|------------------|----------|----------|------------|--------------|-------------|----------------------|
| **Trend Following** | Very Strong | Central bank divergence, economic cycles, momentum | Hours-weeks | Low | Low | Strong directional moves | Ranging/choppy | Low | Moderate | Very High | ✅ PRIMARY RECOMMENDATION |
| **Carry Trade** | Strong | Interest rate differentials, risk premium | Weeks-months | Very Low | Very Low | Stable/risk-on | Risk-off events, crises | Low | Low | High | ✅ Secondary (longer-term) |
| **Mean Reversion** | Moderate | Overreaction, liquidity provision, range-bound markets | Minutes-hours | High | High | Ranging markets | Strong trends, news events | Moderate | High | Moderate | ⚠️ Use selectively |
| **Breakout** | Moderate | Volatility clustering, stop runs, news reactions | Minutes-days | Moderate | Moderate | Volatile periods, news | False breakouts, low vol | Low-Moderate | High | Moderate | ✅ Good for gold |
| **Momentum (Short-term)** | Moderate | Order flow imbalance, institutional flows | Minutes-hours | High | High | High volume periods | Low liquidity, reversals | Moderate | High | Moderate | ⚠️ Needs careful filtering |
| **Volatility Targeting** | Strong | Volatility clustering, risk management | Days-weeks | Low | Low | All regimes | Volatility spikes | Moderate | Low | High | ✅ As overlay |

### Deep Dive: Recommended Initial Strategy - **Trend Following with Volatility Overlay**

**Why This Combination for Forex/Gold:**
1. **Strongest evidence base** - Decades of academic and practical validation in FX
2. **Low turnover** - Critical for forex where spreads eat profits
3. **Works across all three instruments** - EUR/USD, GBP/USD, XAU/USD
4. **Simple implementation** - Few parameters, easy to understand and debug
5. **Scalable** - Works from $500 to $10M+
6. **Robust to overfitting** - Few parameters to optimize
7. **Compatible with 24/5 market** - No overnight gap risk (except weekends)
8. **Gold-specific advantage** - Gold trends strongly during uncertainty

**Underlying Hypothesis:**
Currency markets exhibit momentum due to:
- Central bank policy divergence (slow to change)
- Economic cycle differences between countries
- Behavioral biases (anchoring to old exchange rates)
- Institutional rebalancing delays
- Risk premium for providing liquidity

**Typical Parameters (Daily Bars):**
- Lookback period: 20-100 days for trend identification
- Entry: Price > moving average OR channel breakout
- Exit: Price < moving average OR trailing stop (ATR-based)
- Position sizing: Volatility-targeted (inverse ATR)
- Filter: Only trade during London/NY overlap for intraday entries

**Gold-Specific Adjustments:**
- Wider stops (gold more volatile than currencies)
- Longer lookback periods (gold trends persist longer)
- Consider USD strength index (DXY) as filter
- Monitor real interest rates (TIPS yields)

**Known Failure Modes:**
- Extended sideways markets (whipsaws) - COMMON in summer months
- Sharp reversals (central bank surprises)
- Low volatility environments (false signals)
- High correlation across pairs during crises (diversification fails)
- Weekend gaps (Friday close to Monday open)

**Mitigation Strategies:**
- Volatility filtering (don't trade if ATR < threshold)
- Multiple timeframes (combine daily trend with 4H entry)
- Correlation limits (avoid EUR/USD and GBP/USD simultaneously if highly correlated)
- Drawdown controls (reduce size after losses)
- Weekend risk management (reduce positions before Friday close)

---

## 3. Valid Strategy Definition: Objective Acceptance/Rejection Criteria

### Minimum Requirements (ALL must pass)

| Test | Threshold | Rationale |
|------|-----------|-----------|
| **Sample Size** | ≥300 trades OR ≥5 years hourly data | Statistical significance for forex |
| **In-Sample Sharpe** | ≥0.7 (annualized) | Minimum risk-adjusted return |
| **Out-of-Sample Sharpe** | ≥0.4 (annualized) | Robustness check |
| **Walk-Forward Sharpe** | ≥0.3 (average across windows) | Stability over time |
| **Max Drawdown** | ≤20% (in-sample), ≤30% (out-of-sample) | Conservative for leveraged instruments |
| **Profit Factor** | ≥1.3 (gross profit/gross loss) | Edge verification |
| **Win Rate** | 40-60% (not extreme) | Avoid curve-fitted extremes |
| **Average Win/Loss Ratio** | ≥1.0 OR win rate ≥45% | Mathematical expectancy |
| **Parameter Stability** | ≤30% performance variation across ±20% parameter change | Robustness |
| **Transaction Cost Sensitivity** | Still profitable at 2x estimated spreads | Execution realism |
| **Slippage Sensitivity** | Still profitable at 1.5x estimated slippage | Execution realism |
| **Regime Testing** | Profitable in ≥2 of 3 regimes (trending/ranging/volatile) | Adaptability |
| **Multiple Testing Correction** | Passes deflated Sharpe ratio test (p<0.05) | Data snooping protection |
| **Weekend Gap Test** | Survives typical weekend gaps without catastrophic loss | Forex-specific risk |

### Rejection Criteria (ANY triggers rejection)

- Out-of-sample Sharpe < 0.2
- Walk-forward consistency < 50% of windows profitable
- Maximum drawdown > 35% in any test period
- Profit factor < 1.15 after costs
- Parameter sensitivity > 50% performance variation
- Only works in one market regime
- Requires >4 optimized parameters
- Backtest assumes perfect execution (no spread/slippage)
- Shows signs of look-ahead bias
- Cannot explain economic rationale
- Fails during major news events (NFP, CPI, central bank decisions)

---

## 4. Overfitting: Deep Investigation (Forex-Specific)

### Types of Overfitting in Forex Trading

| Type | Description | Detection Method | Prevention |
|------|-------------|------------------|------------|
| **Look-Ahead Bias** | Using future data (e.g., tomorrow's close) | Code review, timestamp validation | Strict point-in-time data handling |
| **Broker-Specific Bias** | Strategy works only on one broker's data | Test across multiple brokers | Use aggregated data sources |
| **Spread Overfitting** | Optimized for specific spread conditions | Test with variable spreads | Use dynamic spread modeling |
| **Time-of-Day Overfitting** | Only works during specific sessions | Session-by-session analysis | Require cross-session performance |
| **News Event Overfitting** | Avoids all news events artificially | Test including news periods | Explicit news handling rules |
| **Parameter Overfitting** | Too many optimized parameters | Parameter perturbation analysis | Limit to ≤3 parameters |
| **Regime Overfitting** | Works only in specific volatility regime | Multi-regime testing | Require cross-regime performance |

### Recommended Anti-Overfitting Protocol for Forex

1. **Pre-registration**: Document hypothesis before testing
2. **Data Split**: 60% training, 20% validation, 20% holdout (never touch holdout until final)
3. **Embargo**: 10% gap between training and validation periods
4. **Walk-Forward**: Minimum 4 windows, expanding or rolling
5. **Parameter Limits**: Maximum 3 optimized parameters
6. **Perturbation Test**: ±20% parameter variation must maintain >70% performance
7. **Spread Stress Test**: Must be profitable at 2x current spreads
8. **Session Test**: Must work in at least 2 of 3 major sessions (Asian, London, NY)
9. **Regime Test**: Must work in low, medium, and high volatility periods
10. **Final Holdout Test**: Single test on untouched data (pass/fail)

---

## 5. Backtesting Engines: Critical Comparison (Forex Focus)

### Engine Comparison for Forex/Gold

| Engine | Forex Support | Realism | Speed | Flexibility | Community | Maintenance | Live Trading | Learning Curve | Verdict |
|--------|--------------|---------|-------|-------------|-----------|-------------|--------------|----------------|---------|
| **QuantConnect LEAN** | Excellent | Very High | High | Very High | Large | Active | Yes | Steep | ⚠️ Overkill for V1 |
| **QSTrader** | Good | High | Moderate | High | Small | Moderate | Yes | Moderate | ✅ Good candidate |
| **vectorbt** | Good | Moderate | Very High | Moderate | Growing | Active | No | Low | ⚠️ Vectorized only |
| **Backtrader** | Good | High | Moderate | Very High | Large | Dormant | Yes | Moderate | ⚠️ No longer maintained |
| **Custom Event-Driven** | Your design | High | Variable | Very High | None | Your responsibility | Possible | High | ✅ Best long-term |

### Recommendation: **Hybrid Approach**

**V1 (Research):** Use vectorbt for rapid hypothesis testing + custom event-driven for final validation
**V2 (Paper):** Extend custom event-driven engine with realistic forex execution
**V3 (Live):** Integrate with broker API (IBKR, OANDA, etc.)

---

## 6. Data Sources: Forex & Gold Specific

### Forex/Gold Data Providers

| Provider | Historical Data | Real-Time | Cost | Quality | API | Tick Data | Verdict |
|----------|----------------|-----------|------|---------|-----|-----------|---------|
| **Interactive Brokers** | Excellent | Excellent | Free with account | Very High | Yes | Yes | ✅ Best overall |
| **OANDA** | Excellent | Excellent | Free with account | Very High | Yes | Yes | ✅ Great for beginners |
| **Dukascopy** | Excellent | Excellent | Free | Very High | Yes | Yes | ✅ Good free option |
| **TrueFX** | Good | No | Free | High | Yes | Yes | ✅ Free historical |
| **HistData.com** | Excellent | No | $50-200/month | Very High | Download | Yes | ✅ Best paid historical |

### Recommended Data Strategy

**V1 (Research):**
- **Primary**: Dukascopy free historical data (via Python packages)
  - 10+ years of hourly/daily data
  - Good quality for majors
  - Free
- **Backup**: TrueFX for additional validation

**V2/V3 (Paper/Live Trading):**
- **Primary**: Interactive Brokers or OANDA API
  - Free real-time data with account
  - Historical data available
  - Paper trading included
  - Production-ready

---

## 7. Execution Realism: Forex & Gold Specific

### V1 Execution Model (Minimum Viable for Forex/Gold)

```python
# Simplified but realistic execution model for forex
if order_type == "market":
    if is_london_ny_overlap():
        spread = 0.5  # pips for EUR/USD
        slippage = 0.3  # pips
    elif is_asian_session():
        spread = 0.8  # pips
        slippage = 0.5  # pips
    elif is_weekend_opening():
        spread = 2.0  # pips (wider)
        slippage = 1.0  # pips
    else:
        spread = 1.0  # pips (default)
        slippage = 0.5  # pips
    
    # Gold has wider spreads
    if symbol == "XAUUSD":
        spread *= 20  # Convert pips to cents
        slippage *= 20
    
    execution_price = close_price + spread + slippage

# Swap/rollover costs for overnight positions
swap = calculate_swap(symbol, direction, days_held)
```

### Key Insights for Forex/Gold

1. **Spread is the dominant cost** - More important than commissions for retail
2. **Session matters** - London/NY overlap has best execution
3. **News events cause extreme slippage** - Must model or avoid
4. **Weekend gaps are real risk** - Friday close to Monday open
5. **Rollover (5pm ET) spreads widen** - Avoid trading during this period
6. **Gold behaves differently** - Wider spreads, larger moves, different drivers

---

## 8. Technology Stack: Simplified for Forex/Gold Focus

### V1 (Research System - Minimal)

```
Core:
- Python 3.12+
- pandas, numpy, scipy
- scikit-learn (basic models only)
- matplotlib, plotly (visualization)
- pytest (testing)
- pydantic (configuration)
- requests (API calls)

Data Storage:
- CSV/Parquet files (local storage)
- SQLite (lightweight metadata)

Infrastructure:
- Git (version control)
- Virtual environment (venv or conda)
- Jupyter Lab (research notebooks)

Deployment:
- Local machine only
- No Docker required initially
```

### V2 (Paper Trading System)

```
Additions:
- PostgreSQL (structured trade data)
- Docker (reproducibility)
- APScheduler (job scheduling for 24/5 operation)
- Broker SDK (IBKR, OANDA, or similar)
- Enhanced logging (structlog)
```

### V3 (Live Trading System)

```
Additions:
- Enhanced error handling and retry logic
- Redundant data feeds
- Sentry (error tracking)
- Prometheus + Grafana (monitoring)
- Enhanced security (vault, encryption)
- Backup/failover systems
```

---

## 9. Research Pipeline: Forex & Gold Workflow

### Stage-by-Stage Breakdown (Tailored)

#### Stage 1: Hypothesis Definition
**Output:** Written document containing:
- Economic/statistical rationale (e.g., "EUR/USD trends due to ECB/Fed divergence")
- Expected market conditions (trending vs ranging)
- Entry/exit logic (conceptual)
- Risk management approach (position sizing, stops)
- Success criteria (Sharpe, drawdown, etc.)

**Gate:** Hypothesis must have logical basis beyond "it might work"

#### Stage 2: Data Collection
**Activities:**
- Download historical data for EUR/USD, GBP/USD, XAU/USD
- Minimum 5-10 years of hourly data OR 15+ years daily
- Include bid/ask if available
- Document data source and limitations

**Output:** Raw data files with metadata

#### Stage 3: Data Cleaning
**Activities:**
- Handle missing timestamps (forex should be continuous except weekends)
- Remove obvious outliers (>10 standard deviations)
- Validate bid/ask consistency (bid < ask always)
- Check for weekend gaps
- Create session markers (Asian, London, NY)

**Output:** Cleaned dataset with quality report

#### Stage 4: Feature Engineering
**Activities:**
- Calculate technical indicators (MA, ATR, RSI, etc.)
- Generate lagged variables
- Create session-based features
- Calculate volatility measures
- Ensure no look-ahead bias (critical!)

**Output:** Feature matrix with documentation

**Critical Check:** All features must be calculable using only past data

#### Stage 5: Strategy Definition
**Activities:**
- Code entry conditions (e.g., price > MA(50))
- Code exit conditions (e.g., price < MA(20) or trailing stop)
- Define position sizing (e.g., 1% risk per trade, ATR-based)
- Implement risk rules (max daily loss, correlation limits)
- Add transaction cost model (spread + slippage + swap)

**Output:** Strategy class with clear interface

#### Stage 6: Initial Backtest
**Activities:**
- Run on training data (60%)
- Calculate performance metrics
- Generate equity curve
- Analyze trade statistics by session, day of week, etc.

**Output:** Initial performance report

**Gate:** Must meet minimum Sharpe > 0.7 in-sample

#### Stage 7: Cost Model Integration
**Activities:**
- Add realistic spreads (session-dependent)
- Model slippage (0.3-1.0 pips typical)
- Include swap/rollover costs
- Test sensitivity (1x, 1.5x, 2x costs)

**Output:** Cost-adjusted performance

**Gate:** Must remain profitable at 2x estimated costs

#### Stage 8: Out-of-Sample Test
**Activities:**
- Run on validation data (20%)
- Compare to in-sample results
- Calculate performance degradation

**Output:** OOS performance report

**Gate:** OOS Sharpe must be ≥60% of in-sample Sharpe

#### Stage 9: Walk-Forward Testing
**Activities:**
- Define windows (minimum 4, e.g., 2-year train, 6-month test)
- Run expanding or rolling analysis
- Calculate consistency metrics
- Analyze regime performance

**Output:** Walk-forward analysis report

**Gate:** ≥60% of windows must be profitable

#### Stage 10: Robustness Testing
**Activities:**
- Parameter perturbation (±20%)
- Monte Carlo simulation (1000+ runs with randomized entry dates)
- Session analysis (Asian vs London vs NY)
- Different instrument testing (EUR/USD → GBP/USD → XAU/USD)

**Output:** Robustness report

**Gate:** Performance variation <30% across tests

#### Stage 11: Risk Analysis
**Activities:**
- Calculate maximum drawdown
- Analyze worst trades (were they during news?)
- Stress test scenarios (weekend gaps, flash crashes)
- Correlation analysis (EUR/USD vs GBP/USD)
- Tail risk metrics (VaR, CVaR)

**Output:** Risk report

**Gate:** Max drawdown <20% in all tests

#### Stage 12: Final Holdout Test
**Activities:**
- Run on untouched holdout data (20%)
- Single test only (no optimization)
- Compare to all previous results

**Output:** Final validation report

**Gate:** Holdout Sharpe > 0.4, otherwise REJECT strategy

#### Stage 13: Decision Gate
**Possible Outcomes:**
- ✅ PASS → Proceed to paper trading
- ⚠️ MARGINAL → Refine hypothesis, restart
- ❌ FAIL → Reject strategy, document learnings

#### Stage 14: Paper Trading
**Activities:**
- Deploy to paper trading environment (IBKR or OANDA)
- Run with real-time data
- Monitor execution quality (actual vs modeled spread)
- Track slippage vs. estimates
- Collect minimum 50 trades or 3 months

**Output:** Paper trading performance report

**Gate:** Paper results within 20% of backtest expectations

#### Stage 15: Live Evaluation (Future)
**Activities:**
- Small capital deployment ($100-500 initially)
- Intensive monitoring
- Regular performance review
- Scale up gradually if successful

---

## 10. Unknowns / Questions Requiring Further Research

### Critical Unknowns for Forex/Gold

1. **Optimal Parameter Ranges for Each Pair**
   - What lookback periods work best for EUR/USD vs GBP/USD vs XAU/USD?
   - Need empirical testing across multiple years

2. **Realistic Slippage Estimates by Session**
   - Actual slippage varies by broker, time of day, news events
   - Need paper trading data to calibrate models

3. **Best Approach for Weekend Gap Risk**
   - Close all positions Friday? Reduce size? Hedge?
   - Need analysis of historical weekend gaps

4. **News Event Impact Quantification**
   - How much do NFP, CPI, central bank decisions affect execution?
   - Should we avoid trading during these events?

5. **Optimal Position Sizing for Leveraged Instruments**
   - Kelly criterion too aggressive for forex?
   - Fixed fractional vs. volatility targeting?
   - Need testing across account sizes

6. **Correlation Behavior During Crises**
   - Do EUR/USD and GBP/USD become perfectly correlated during risk-off?
   - Does gold still provide diversification?

7. **Broker-to-Broker Execution Differences**
   - How much do spreads and slippage vary between brokers?
   - Should we test across multiple brokers?

### Questions for User Decision

1. **What is your available capital?**
   - <$500: Very limited options, high risk
   - $500-$2,000: Micro lots feasible
   - $2,000-$10,000: Standard lots possible
   - $10,000+: Full flexibility

2. **What leverage will you use?**
   - Conservative: 5:1 to 10:1 (recommended)
   - Moderate: 10:1 to 30:1
   - Aggressive: 30:1+ (NOT recommended)

3. **Which broker will you use?**
   - Interactive Brokers (best overall)
   - OANDA (beginner-friendly)
   - Others? (must have API access)

4. **What is your risk tolerance?**
   - Maximum acceptable drawdown? (suggest ≤20%)
   - Time horizon for recovery?

5. **What is your time commitment?**
   - Full-time research vs. part-time?
   - Will you monitor trades or fully automate?

6. **What is your primary goal?**
   - Income generation?
   - Capital appreciation?
   - Learning/research?
   - Prop firm funding?

---

## 11. Final Recommendations (Forex & Gold Focused)

### 1. Recommended Instruments
**Primary:** EUR/USD, GBP/USD, XAU/USD
**Secondary (future):** AUD/USD, USD/CAD, XAG/USD
**Avoid initially:** Exotic pairs, EUR/GBP, crypto CFDs

### 2. Recommended Initial Strategy Family
**Trend Following with Volatility Overlay**
- Rationale: Strongest evidence base, low complexity, robust to overfitting
- Specific approach: Moving average crossover or channel breakout with ATR-based position sizing
- Timeframe: Daily bars for direction, 4-hour or 1-hour for entry timing

### 3. Recommended Timeframe
**Primary:** Daily bars for trend identification
**Secondary:** 4-hour bars for entry refinement
**Rationale:** Lower transaction costs, less noise, easier to model, compatible with part-time monitoring

### 4. Recommended Data Source
**V1:** Dukascopy free historical data (via Python packages like `dukascopy` or `findatapy`)
**V2/V3:** Interactive Brokers or OANDA API (free real-time with account)
**Rationale:** Free high-quality data for research, production-ready for live

### 5. Recommended Backtesting Framework
**V1:** Hybrid approach
- vectorbt for rapid initial research
- Custom event-driven (based on QSTrader patterns) for final validation
**V2:** Extended custom event-driven engine with forex-specific execution
**V3:** Direct broker API integration

### 6. Recommended Technology Stack

**V1 (Research):**
```
- Python 3.12+
- pandas, numpy, scipy
- scikit-learn (basic)
- matplotlib, plotly
- pytest
- pydantic
- Jupyter Lab
- SQLite (metadata)
- Parquet files (data)
- dukascopy/findatapy (data download)
```

**V2 (Paper):** Add PostgreSQL, Docker, APScheduler, broker SDK
**V3 (Live):** Add enhanced monitoring, error tracking, redundancy

### 7. Recommended Risk Architecture
**Three-layer system:**
1. **Strategy-level:** Stop losses (ATR-based), position limits per trade (1-2% risk)
2. **Portfolio-level:** Maximum exposure (e.g., 3 positions max), correlation limits (no more than 2 highly correlated pairs)
3. **System-level:** Daily loss limit (3-5%), maximum drawdown circuit breaker (15-20%), weekend position reduction, emergency kill switch

**Key principle:** Risk management independent from strategy logic, can override any signal

**Forex-Specific Rules:**
- Reduce or close positions before Friday close (weekend gap risk)
- Avoid trading during major news events (or reduce size significantly)
- Monitor correlation between EUR/USD and GBP/USD (often move together)
- Gold position sizes should be smaller due to higher volatility

### 8. Recommended Validation Methodology
**Sequential gates:**
1. In-sample test (Sharpe > 0.7)
2. Out-of-sample test (Sharpe > 0.4, ≥60% of IS)
3. Walk-forward test (≥60% windows profitable)
4. Parameter sensitivity (≤30% variation)
5. Cost stress test (profitable at 2x spreads)
6. Session test (works in London and/or NY sessions)
7. Regime test (works in trending and ranging markets)
8. Final holdout test (single test, Sharpe > 0.4)
9. Paper trading (50+ trades, within 20% of backtest)

### 9. Recommended Paper-Trading Approach
**Identical to backtest engine with:**
- Real-time data feed from broker
- Simulated order execution with realistic spreads/slippage
- Same risk management rules
- Performance tracking identical to live
- Minimum 3 months or 50 trades before live consideration
- **Critical:** Compare actual execution to modeled execution

### 10. Minimal V1 Architecture

```
forex_gold_trading/
├── config/
│   ├── settings.py
│   └── .env.example
├── data/
│   ├── raw/
│   │   └── (downloaded from Dukascopy)
│   ├── processed/
│   └── features/
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   ├── cleaner.py
│   │   └── downloader.py  # Dukascopy API
│   ├── features/
│   │   └── engineering.py
│   ├── strategies/
│   │   ├── base.py
│   │   └── trend_following.py
│   ├── backtesting/
│   │   ├── engine.py
│   │   ├── execution.py  # Forex-specific spread/slippage
│   │   └── costs.py  # Spread, swap, slippage
│   ├── risk/
│   │   └── manager.py
│   ├── utils/
│   │   ├── metrics.py
│   │   └── sessions.py  # Asian/London/NY session detection
│   └── config/
│       └── settings.py
├── tests/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_strategy_research.ipynb
│   └── 03_validation.ipynb
├── reports/
├── requirements.txt
└── README.md
```

### 11. Future V2 Architecture (Paper Trading)

```
Additions:
├── src/
│   ├── live/
│   │   ├── data_handler.py  # Real-time from broker
│   │   ├── paper_executor.py
│   │   └── monitor.py
│   └── portfolio/
│       └── tracker.py
├── docker/
│   └── Dockerfile
├── scheduler/
│   └── jobs.py  # 24/5 operation
└── database/
    └── models.py (PostgreSQL)
```

### 12. Future V3 Architecture (Live Trading)

```
Additions:
├── src/
│   ├── live/
│   │   ├── broker_connector.py  # IBKR/OANDA API
│   │   ├── order_manager.py
│   │   └── reconciliation.py
│   └── monitoring/
│       ├── alerts.py
│       └── dashboard.py
├── infrastructure/
│   ├── backup_feeds/
│   └── failover/
└── security/
    └── vault_integration.py
```

---

## Conclusion

This research phase has been **specifically tailored** to Forex and Gold trading:

1. ✅ **Asset class focus narrowed** to EUR/USD, GBP/USD, XAU/USD
2. ✅ **Strategy evaluation** specific to currency market dynamics
3. ✅ **Execution modeling** includes spreads, swaps, session variations
4. ✅ **Data sources** identified for forex/gold (Dukascopy, IBKR, OANDA)
5. ✅ **Risk management** includes weekend gaps, news events, correlation
6. ✅ **Validation methodology** accounts for forex-specific challenges
7. ✅ **Technology stack** simplified for focused scope
8. ✅ **Research pipeline** designed for currency markets
9. ✅ **Unknowns acknowledged** requiring further investigation

**Next Step:** Present this architecture to you for approval before beginning ANY implementation.

**Do you approve this forex & gold-focused research and architecture, or would you like me to investigate any specific area further before proceeding?**

Key questions to confirm before implementation:
1. What is your available capital?
2. Which broker will you use (IBKR, OANDA, other)?
3. What leverage will you employ (recommend 5:1 to 10:1)?
4. What is your maximum acceptable drawdown?
5. Will you trade part-time or full-time?
