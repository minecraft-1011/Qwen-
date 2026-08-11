"""Strategies module initialization"""
from .base import (
    Signal,
    BaseStrategy,
    TrendFollowingStrategy,
    get_strategy,
)

__all__ = [
    'Signal',
    'BaseStrategy',
    'TrendFollowingStrategy',
    'get_strategy',
]
