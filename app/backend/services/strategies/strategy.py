"""
Base trading strategy interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class TradingStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def generate_signals(
        self,
        tickers: List[str],
        current_date: str,
        lookback_start: str,
        portfolio: Dict[str, Any],
        current_prices: Dict[str, float],
        request: Dict[str, Any] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate trading signals for given tickers.
        
        Args:
            tickers: List of ticker symbols
            current_date: Current date string (YYYY-MM-DD)
            lookback_start: Start date for lookback period (YYYY-MM-DD)
            portfolio: Current portfolio state
            current_prices: Current prices for all tickers
            request: Request object containing API keys and other metadata
            
        Returns:
            Dict mapping ticker to decision dict with 'action' and 'quantity' keys
            Example: {'AAPL': {'action': 'buy', 'quantity': 100}}
        """
        pass
    
    @abstractmethod
    def get_strategy_info(self) -> Dict[str, Any]:
        """
        Get information about this strategy.
        
        Returns:
            Dict containing strategy metadata
        """
        pass


class StrategyResult:
    """
    Container for strategy execution results.
    """
    
    def __init__(
        self,
        decisions: Dict[str, Dict[str, Any]],
        signals: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None
    ):
        self.decisions = decisions
        self.signals = signals or {}
        self.metadata = metadata or {}
