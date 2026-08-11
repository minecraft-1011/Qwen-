"""
Test configuration and basic imports
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def test_config_loads():
    """Test that configuration loads correctly"""
    from config import TradingSystemConfig
    
    # Load with defaults (no .env file)
    config = TradingSystemConfig.load_from_env()
    
    assert config.trading_mode == 'paper', "Default mode should be paper"
    assert config.funding_pips.max_daily_loss_percent == 5.0
    assert config.funding_pips.effective_daily_loss_limit == 4.0
    assert config.risk.max_leverage == 10
    assert config.risk.risk_per_trade_percent == 0.5
    
    print("✅ Configuration tests passed")


def test_risk_manager():
    """Test risk manager functionality"""
    from risk.manager import RiskManager, RiskLimits
    
    # Create risk manager with FundingPips limits
    config = RiskLimits(
        max_daily_loss_percent=5.0,
        max_total_loss_percent=10.0,
        profit_target_percent=8.0,
        daily_loss_buffer=1.0,
        total_loss_buffer=1.0,
    )
    
    rm = RiskManager(config)
    rm.starting_balance = 10000.0
    rm.current_balance = 10000.0
    
    # Test initial state
    status = rm.check_risk_limits()
    assert status.trading_allowed == True, "Should allow trading initially"
    
    # Simulate losses
    rm.daily_start_balance = 10000.0
    rm.current_balance = 9600.0  # 4% loss
    
    status = rm.check_risk_limits()
    assert status.trading_allowed == False, "Should block after 4% daily loss"
    assert 'Daily loss limit' in status.reason_blocked
    
    print("✅ Risk manager tests passed")


def test_strategy_creation():
    """Test strategy creation"""
    from strategies.base import get_strategy, TrendFollowingStrategy
    
    # Create trend following strategy
    config = {
        'fast_period': 20,
        'slow_period': 50,
        'atr_period': 14,
        'risk_per_trade': 0.005,
    }
    
    strategy = get_strategy('trend_following', config)
    
    assert isinstance(strategy, TrendFollowingStrategy)
    assert strategy.fast_period == 20
    assert strategy.slow_period == 50
    
    print("✅ Strategy tests passed")


def test_feature_engineering():
    """Test feature engineering"""
    import pandas as pd
    import numpy as np
    from features.engineering import FeatureEngineer
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    df = pd.DataFrame({
        'open': 1.1 + np.cumsum(np.random.randn(100) * 0.001),
        'high': 1.1 + np.cumsum(np.random.randn(100) * 0.001) + 0.002,
        'low': 1.1 + np.cumsum(np.random.randn(100) * 0.001) - 0.002,
        'close': 1.1 + np.cumsum(np.random.randn(100) * 0.001),
        'volume': np.random.randint(1000, 10000, 100),
    }, index=dates)
    
    # Add features
    fe = FeatureEngineer()
    df_with_features = fe.add_all_features(df)
    
    # Check features were added
    assert 'sma_20' in df_with_features.columns
    assert 'ema_20' in df_with_features.columns
    assert 'rsi_14' in df_with_features.columns
    assert 'macd_line' in df_with_features.columns
    assert 'atr_14' in df_with_features.columns
    
    print("✅ Feature engineering tests passed")


def test_data_loader():
    """Test data loader with sample data"""
    from datetime import datetime
    from data.loader import DataDownloader, DataCleaner
    
    downloader = DataDownloader(Path(__file__).parent.parent / 'data')
    
    # Generate sample data
    start = datetime(2023, 1, 1)
    end = datetime(2024, 1, 1)
    
    df = downloader._generate_sample_data('EUR/USD', start, end, 'D1')
    
    assert len(df) > 0
    assert 'open' in df.columns
    assert 'high' in df.columns
    assert 'low' in df.columns
    assert 'close' in df.columns
    assert 'volume' in df.columns
    
    # Test cleaner
    cleaner = DataCleaner()
    cleaned = cleaner.clean_ohlcv(df)
    
    assert len(cleaned) == len(df)
    assert not cleaned.isnull().any().any()
    
    print("✅ Data loader tests passed")


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Running FundingPips Trading System Tests")
    print("="*50 + "\n")
    
    try:
        test_config_loads()
        test_risk_manager()
        test_strategy_creation()
        test_feature_engineering()
        test_data_loader()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED ✅")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
