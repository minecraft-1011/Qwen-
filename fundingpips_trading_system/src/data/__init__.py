"""Data module initialization"""
from .loader import (
    DataDownloader,
    DataCleaner,
    load_instrument_data,
    load_eurusd_data,
    load_gbpusd_data,
    load_xauusd_data,
    load_all_instruments,
)

__all__ = [
    'DataDownloader',
    'DataCleaner',
    'load_instrument_data',
    'load_eurusd_data',
    'load_gbpusd_data',
    'load_xauusd_data',
    'load_all_instruments',
]
