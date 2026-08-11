"""
Data Module for FundingPips Trading System

Handles downloading, cleaning, and managing market data.
Primary source: Dukascopy (free, high-quality forex data)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import warnings


class DataDownloader:
    """Download historical forex and gold data from Dukascopy"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Dukascopy base URL for tick data
        self.base_url = "https://datafeed.dukascopy.com/search/feed/data/v1/download"
        
        # Instrument mappings (Dukascopy uses specific codes)
        self.instrument_map = {
            'EUR/USD': {'symbol': 'EURUSD', 'market': 'FOREX'},
            'GBP/USD': {'symbol': 'GBPUSD', 'market': 'FOREX'},
            'XAU/USD': {'symbol': 'XAUUSD', 'market': 'METAL'},
        }
    
    def download_dukascopy_data(
        self,
        instrument: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str = 'D1'
    ) -> pd.DataFrame:
        """
        Download data from Dukascopy
        
        Note: This is a simplified implementation. For production use,
        consider using the official Dukascopy Python library or
        downloading CSV files manually from their website.
        
        Alternative: Use the `duka` command-line tool to download data,
        then load it with load_local_data()
        """
        print(f"Downloading {instrument} data from {start_date} to {end_date}")
        print("Note: Using sample data generator. For real data, use:")
        print("  1. Manual download from dukascopy.com")
        print("  2. duka CLI tool: https://github.com/AdmiralMarkets/duka")
        print("  3. OANDA API (requires free demo account)")
        
        # Generate sample data for development/testing
        return self._generate_sample_data(
            instrument, start_date, end_date, timeframe
        )
    
    def _generate_sample_data(
        self,
        instrument: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str
    ) -> pd.DataFrame:
        """Generate realistic sample data for testing"""
        
        # Date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Base price and volatility by instrument
        params = {
            'EUR/USD': {'base': 1.1000, 'volatility': 0.006},
            'GBP/USD': {'base': 1.2700, 'volatility': 0.008},
            'XAU/USD': {'base': 1950.0, 'volatility': 0.015},
        }
        
        if instrument not in params:
            raise ValueError(f"Unknown instrument: {instrument}")
        
        base_price = params[instrument]['base']
        daily_vol = params[instrument]['volatility']
        
        # Generate returns with slight trend and mean reversion
        np.random.seed(42)  # For reproducibility
        n_days = len(dates)
        
        # Random walk with drift
        returns = np.random.normal(0.0001, daily_vol, n_days)
        
        # Add some autocorrelation (momentum)
        returns = pd.Series(returns).rolling(5, min_periods=1).mean().values
        
        # Calculate prices
        prices = base_price * (1 + np.cumsum(returns))
        
        # Generate OHLC from close prices
        df = pd.DataFrame({
            'date': dates,
            'close': prices
        })
        
        # Add intraday variation for OHLC
        intraday_range = prices * daily_vol * 0.5
        df['high'] = df['close'] + np.abs(np.random.normal(0, 1, n_days)) * intraday_range
        df['low'] = df['close'] - np.abs(np.random.normal(0, 1, n_days)) * intraday_range
        df['open'] = df['close'] + np.random.normal(0, 1, n_days) * intraday_range * 0.3
        
        # Ensure OHLC consistency
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)
        
        # Volume (random, higher on weekdays)
        df['volume'] = np.random.randint(1000, 10000, n_days)
        df['volume'] = df['volume'] * (1 + (df['date'].dt.dayofweek < 5) * 0.5)
        
        # Set index
        df.set_index('date', inplace=True)
        
        return df
    
    def load_local_data(
        self,
        instrument: str,
        timeframe: str = 'D1'
    ) -> Optional[pd.DataFrame]:
        """Load previously downloaded data from disk"""
        
        filename = f"{instrument.replace('/', '_')}_{timeframe}.csv"
        filepath = self.raw_dir / filename
        
        if not filepath.exists():
            return None
        
        df = pd.read_csv(filepath, index_col='date', parse_dates=True)
        return df
    
    def save_data(self, df: pd.DataFrame, instrument: str, timeframe: str = 'D1'):
        """Save processed data to disk"""
        
        filename = f"{instrument.replace('/', '_')}_{timeframe}.csv"
        filepath = self.raw_dir / filename
        
        df.to_csv(filepath)
        print(f"Saved data to {filepath}")


class DataCleaner:
    """Clean and validate market data"""
    
    def __init__(self):
        pass
    
    def clean_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean OHLCV data
        
        Checks:
        - Missing values
        - Negative prices
        - High > Low violations
        - Outliers
        - Duplicates
        """
        df = df.copy()
        
        # Remove duplicates
        initial_len = len(df)
        df = df[~df.index.duplicated(keep='first')]
        if len(df) < initial_len:
            warnings.warn(f"Removed {initial_len - len(df)} duplicate rows")
        
        # Check for negative prices
        if (df[['open', 'high', 'low', 'close']] < 0).any().any():
            raise ValueError("Negative prices detected")
        
        # Fix OHLC inconsistencies
        inconsistent = df['high'] < df['low']
        if inconsistent.any():
            warnings.warn(f"Fixed {inconsistent.sum()} OHLC inconsistencies")
            # Swap high and low where needed
            df.loc[inconsistent, ['high', 'low']] = df.loc[inconsistent, ['low', 'high']].values
        
        # Ensure high >= open, close and low <= open, close
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)
        
        # Handle missing values
        if df.isnull().any().any():
            warnings.warn("Interpolating missing values")
            df = df.interpolate(method='linear')
            df = df.fillna(method='ffill')
            df = df.fillna(method='bfill')
        
        # Detect outliers (more than 5 standard deviations)
        for col in ['open', 'high', 'low', 'close']:
            mean = df[col].mean()
            std = df[col].std()
            outliers = np.abs(df[col] - mean) > 5 * std
            if outliers.any():
                warnings.warn(f"Detected {outliers.sum()} outliers in {col}")
                # Replace with previous value
                df.loc[outliers, col] = df[col].shift(1)
        
        return df
    
    def check_data_quality(self, df: pd.DataFrame) -> Dict:
        """Generate data quality report"""
        
        report = {
            'total_rows': len(df),
            'date_range': (df.index.min(), df.index.max()),
            'missing_values': df.isnull().sum().to_dict(),
            'negative_prices': (df[['open', 'high', 'low', 'close']] < 0).any().any(),
            'ohlc_violations': ((df['high'] < df['low']).sum()),
            'zero_volume': (df['volume'] == 0).sum() if 'volume' in df.columns else 0,
            'duplicate_dates': df.index.duplicated().sum(),
        }
        
        return report


def load_instrument_data(
    instrument: str,
    start_date: datetime,
    end_date: datetime,
    timeframe: str = 'D1',
    data_dir: Optional[Path] = None,
    download_if_missing: bool = True
) -> pd.DataFrame:
    """
    Main function to load instrument data
    
    Args:
        instrument: e.g., 'EUR/USD', 'XAU/USD'
        start_date: Start of data range
        end_date: End of data range
        timeframe: 'D1', 'H4', etc.
        data_dir: Base data directory
        download_if_missing: Whether to download if not found locally
    
    Returns:
        DataFrame with OHLCV data
    """
    
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"
    
    downloader = DataDownloader(data_dir)
    cleaner = DataCleaner()
    
    # Try to load from disk first
    df = downloader.load_local_data(instrument, timeframe)
    
    if df is None and download_if_missing:
        # Download new data
        print(f"Data not found locally, downloading {instrument}...")
        df = downloader.download_dukascopy_data(
            instrument, start_date, end_date, timeframe
        )
        downloader.save_data(df, instrument, timeframe)
    elif df is None:
        raise FileNotFoundError(
            f"No data found for {instrument}. Set download_if_missing=True or download manually."
        )
    
    # Filter to date range
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    
    # Clean data
    df = cleaner.clean_ohlcv(df)
    
    # Print quality report
    quality = cleaner.check_data_quality(df)
    print(f"\nData Quality Report for {instrument}:")
    print(f"  Rows: {quality['total_rows']}")
    print(f"  Date Range: {quality['date_range'][0]} to {quality['date_range'][1]}")
    print(f"  Missing Values: {sum(quality['missing_values'].values())}")
    print(f"  OHLC Violations: {quality['ohlc_violations']}")
    
    return df


# Convenience functions for common instruments

def load_eurusd_data(start_date: datetime, end_date: datetime, **kwargs) -> pd.DataFrame:
    """Load EUR/USD data"""
    return load_instrument_data('EUR/USD', start_date, end_date, **kwargs)


def load_gbpusd_data(start_date: datetime, end_date: datetime, **kwargs) -> pd.DataFrame:
    """Load GBP/USD data"""
    return load_instrument_data('GBP/USD', start_date, end_date, **kwargs)


def load_xauusd_data(start_date: datetime, end_date: datetime, **kwargs) -> pd.DataFrame:
    """Load XAU/USD (Gold) data"""
    return load_instrument_data('XAU/USD', start_date, end_date, **kwargs)


def load_all_instruments(
    start_date: datetime,
    end_date: datetime,
    instruments: List[str] = None,
    **kwargs
) -> Dict[str, pd.DataFrame]:
    """Load multiple instruments at once"""
    
    if instruments is None:
        instruments = ['EUR/USD', 'GBP/USD', 'XAU/USD']
    
    data = {}
    for instrument in instruments:
        print(f"\nLoading {instrument}...")
        try:
            data[instrument] = load_instrument_data(
                instrument, start_date, end_date, **kwargs
            )
        except Exception as e:
            warnings.warn(f"Failed to load {instrument}: {e}")
    
    return data
