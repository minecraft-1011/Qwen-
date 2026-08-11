"""
Feature Engineering Module for FundingPips Trading System

Creates technical indicators and features for trading strategies.
All features are designed to avoid look-ahead bias.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional


class FeatureEngineer:
    """Generate technical analysis features"""
    
    def __init__(self):
        pass
    
    def add_moving_averages(
        self,
        df: pd.DataFrame,
        periods: List[int] = [10, 20, 50, 100, 200],
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add simple moving averages"""
        
        df = df.copy()
        for period in periods:
            col_name = f'sma_{period}'
            df[col_name] = df[price_col].rolling(window=period, min_periods=period).mean()
        
        return df
    
    def add_exponential_moving_averages(
        self,
        df: pd.DataFrame,
        periods: List[int] = [10, 20, 50, 100, 200],
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add exponential moving averages"""
        
        df = df.copy()
        for period in periods:
            col_name = f'ema_{period}'
            df[col_name] = df[price_col].ewm(span=period, adjust=False).mean()
        
        return df
    
    def add_rsi(
        self,
        df: pd.DataFrame,
        periods: List[int] = [14],
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add Relative Strength Index"""
        
        df = df.copy()
        for period in periods:
            delta = df[price_col].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            df[f'rsi_{period}'] = rsi
        
        return df
    
    def add_macd(
        self,
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add MACD indicator"""
        
        df = df.copy()
        
        ema_fast = df[price_col].ewm(span=fast, adjust=False).mean()
        ema_slow = df[price_col].ewm(span=slow, adjust=False).mean()
        
        df['macd_line'] = ema_fast - ema_slow
        df['macd_signal'] = df['macd_line'].ewm(span=signal, adjust=False).mean()
        df['macd_histogram'] = df['macd_line'] - df['macd_signal']
        
        return df
    
    def add_bollinger_bands(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: float = 2.0,
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add Bollinger Bands"""
        
        df = df.copy()
        
        df['bb_middle'] = df[price_col].rolling(window=period, min_periods=period).mean()
        rolling_std = df[price_col].rolling(window=period, min_periods=period).std()
        
        df['bb_upper'] = df['bb_middle'] + (rolling_std * std_dev)
        df['bb_lower'] = df['bb_middle'] - (rolling_std * std_dev)
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        df['bb_percent'] = (df[price_col] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        return df
    
    def add_atr(
        self,
        df: pd.DataFrame,
        periods: List[int] = [14],
    ) -> pd.DataFrame:
        """Add Average True Range"""
        
        df = df.copy()
        
        high = df['high']
        low = df['low']
        close_prev = df['close'].shift(1)
        
        tr1 = high - low
        tr2 = abs(high - close_prev)
        tr3 = abs(low - close_prev)
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        for period in periods:
            df[f'atr_{period}'] = true_range.rolling(window=period, min_periods=period).mean()
        
        return df
    
    def add_volatility(
        self,
        df: pd.DataFrame,
        periods: List[int] = [10, 20],
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add historical volatility (standard deviation of returns)"""
        
        df = df.copy()
        returns = df[price_col].pct_change()
        
        for period in periods:
            col_name = f'volatility_{period}'
            df[col_name] = returns.rolling(window=period, min_periods=period).std()
        
        return df
    
    def add_momentum(
        self,
        df: pd.DataFrame,
        periods: List[int] = [10, 20, 50],
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add momentum (rate of change)"""
        
        df = df.copy()
        
        for period in periods:
            col_name = f'momentum_{period}'
            df[col_name] = (df[price_col] / df[price_col].shift(period) - 1) * 100
        
        return df
    
    def add_trend_strength(
        self,
        df: pd.DataFrame,
        short_period: int = 10,
        long_period: int = 50,
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add trend strength indicator"""
        
        df = df.copy()
        
        sma_short = df[price_col].rolling(window=short_period, min_periods=short_period).mean()
        sma_long = df[price_col].rolling(window=long_period, min_periods=long_period).mean()
        
        # Trend strength as percentage difference between MAs
        df['trend_strength'] = ((sma_short - sma_long) / sma_long) * 100
        
        # Trend direction (1 = uptrend, -1 = downtrend, 0 = no trend)
        df['trend_direction'] = np.sign(sma_short - sma_long)
        
        return df
    
    def add_support_resistance(
        self,
        df: pd.DataFrame,
        lookback: int = 20,
    ) -> pd.DataFrame:
        """Add support and resistance levels (rolling high/low)"""
        
        df = df.copy()
        
        df['resistance'] = df['high'].rolling(window=lookback, min_periods=lookback).max()
        df['support'] = df['low'].rolling(window=lookback, min_periods=lookback).min()
        df['range_position'] = (df['close'] - df['support']) / (df['resistance'] - df['support'])
        
        return df
    
    def add_volume_features(
        self,
        df: pd.DataFrame,
        periods: List[int] = [10, 20],
    ) -> pd.DataFrame:
        """Add volume-based features"""
        
        df = df.copy()
        
        if 'volume' not in df.columns:
            return df
        
        for period in periods:
            vol_ma = df['volume'].rolling(window=period, min_periods=period).mean()
            df[f'volume_ratio_{period}'] = df['volume'] / vol_ma
        
        return df
    
    def add_all_features(
        self,
        df: pd.DataFrame,
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """Add all available features"""
        
        df = self.add_moving_averages(df, price_col=price_col)
        df = self.add_exponential_moving_averages(df, price_col=price_col)
        df = self.add_rsi(df, price_col=price_col)
        df = self.add_macd(df, price_col=price_col)
        df = self.add_bollinger_bands(df, price_col=price_col)
        df = self.add_atr(df)
        df = self.add_volatility(df, price_col=price_col)
        df = self.add_momentum(df, price_col=price_col)
        df = self.add_trend_strength(df, price_col=price_col)
        df = self.add_support_resistance(df)
        df = self.add_volume_features(df)
        
        return df


def create_features(
    df: pd.DataFrame,
    feature_list: List[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Create specified features
    
    Args:
        df: DataFrame with OHLCV data
        feature_list: List of features to create (or None for all)
        **kwargs: Additional parameters
    
    Returns:
        DataFrame with added features
    """
    
    fe = FeatureEngineer()
    
    if feature_list is None:
        return fe.add_all_features(df)
    
    df_out = df.copy()
    
    for feature in feature_list:
        if feature == 'sma':
            df_out = fe.add_moving_averages(df_out, **kwargs)
        elif feature == 'ema':
            df_out = fe.add_exponential_moving_averages(df_out, **kwargs)
        elif feature == 'rsi':
            df_out = fe.add_rsi(df_out, **kwargs)
        elif feature == 'macd':
            df_out = fe.add_macd(df_out, **kwargs)
        elif feature == 'bollinger':
            df_out = fe.add_bollinger_bands(df_out, **kwargs)
        elif feature == 'atr':
            df_out = fe.add_atr(df_out, **kwargs)
        elif feature == 'volatility':
            df_out = fe.add_volatility(df_out, **kwargs)
        elif feature == 'momentum':
            df_out = fe.add_momentum(df_out, **kwargs)
        elif feature == 'trend':
            df_out = fe.add_trend_strength(df_out, **kwargs)
        else:
            raise ValueError(f"Unknown feature: {feature}")
    
    return df_out
