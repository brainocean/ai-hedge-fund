"""
Rule-based trading strategy using technical indicators.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from app.backend.services.strategies.strategy import TradingStrategy
from src.tools.api import get_price_data


class RuleStrategy(TradingStrategy):
    """
    Rule-based trading strategy using technical indicators like MACD, RSI, etc.
    """
    
    def __init__(self, rules_config: Dict[str, Any] = None):
        super().__init__("Rule Strategy")
        self.rules_config = rules_config or self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for rule-based strategy."""
        return {
            "macd": {
                "enabled": True,
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9,
                "weight": 0.4
            },
            "rsi": {
                "enabled": True,
                "period": 14,
                "overbought": 70,
                "oversold": 30,
                "weight": 0.3
            },
            "moving_average": {
                "enabled": True,
                "short_period": 20,
                "long_period": 50,
                "weight": 0.3
            },
            "position_sizing": {
                "max_position_pct": 0.1,  # 10% of portfolio per position
                "risk_per_trade": 0.02    # 2% risk per trade
            }
        }
    
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
        Generate trading signals using technical indicators.
        """
        decisions = {}
        
        for ticker in tickers:
            try:
                # Get historical price data
                price_data = get_price_data(ticker, lookback_start, current_date)
                
                if price_data.empty or len(price_data) < 50:
                    decisions[ticker] = {"action": "hold", "quantity": 0}
                    continue
                
                # Calculate technical indicators
                signals = self._calculate_signals(price_data)
                
                # Generate trading decision
                decision = self._make_decision(
                    ticker, signals, portfolio, current_prices[ticker]
                )
                decisions[ticker] = decision
                
            except Exception as e:
                print(f"Error calculating signals for {ticker}: {e}")
                decisions[ticker] = {"action": "hold", "quantity": 0}
        
        return decisions
    
    def _calculate_signals(self, price_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicator signals."""
        signals = {}
        
        # MACD Signal
        if self.rules_config["macd"]["enabled"]:
            macd_signal = self._calculate_macd_signal(price_data)
            signals["macd"] = macd_signal * self.rules_config["macd"]["weight"]
        
        # RSI Signal
        if self.rules_config["rsi"]["enabled"]:
            rsi_signal = self._calculate_rsi_signal(price_data)
            signals["rsi"] = rsi_signal * self.rules_config["rsi"]["weight"]
        
        # Moving Average Signal
        if self.rules_config["moving_average"]["enabled"]:
            ma_signal = self._calculate_ma_signal(price_data)
            signals["ma"] = ma_signal * self.rules_config["moving_average"]["weight"]
        
        return signals
    
    def _calculate_macd_signal(self, price_data: pd.DataFrame) -> float:
        """Calculate MACD signal (-1 to 1)."""
        config = self.rules_config["macd"]
        
        # Calculate MACD
        exp1 = price_data['close'].ewm(span=config["fast_period"]).mean()
        exp2 = price_data['close'].ewm(span=config["slow_period"]).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=config["signal_period"]).mean()
        histogram = macd - signal_line
        
        if len(histogram) < 2:
            return 0.0
        
        # Signal based on MACD line crossing signal line
        current_hist = histogram.iloc[-1]
        prev_hist = histogram.iloc[-2]
        
        if current_hist > 0 and prev_hist <= 0:
            return 1.0  # Bullish crossover
        elif current_hist < 0 and prev_hist >= 0:
            return -1.0  # Bearish crossover
        elif current_hist > 0:
            return 0.5  # Above signal line
        elif current_hist < 0:
            return -0.5  # Below signal line
        else:
            return 0.0
    
    def _calculate_rsi_signal(self, price_data: pd.DataFrame) -> float:
        """Calculate RSI signal (-1 to 1)."""
        config = self.rules_config["rsi"]
        
        # Calculate RSI
        delta = price_data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=config["period"]).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=config["period"]).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        if len(rsi) == 0:
            return 0.0
        
        current_rsi = rsi.iloc[-1]
        
        if current_rsi < config["oversold"]:
            return 1.0  # Oversold - buy signal
        elif current_rsi > config["overbought"]:
            return -1.0  # Overbought - sell signal
        elif current_rsi < 50:
            return 0.3  # Slightly bearish
        elif current_rsi > 50:
            return -0.3  # Slightly bullish
        else:
            return 0.0
    
    def _calculate_ma_signal(self, price_data: pd.DataFrame) -> float:
        """Calculate Moving Average signal (-1 to 1)."""
        config = self.rules_config["moving_average"]
        
        # Calculate moving averages
        short_ma = price_data['close'].rolling(window=config["short_period"]).mean()
        long_ma = price_data['close'].rolling(window=config["long_period"]).mean()
        
        if len(short_ma) < 2 or len(long_ma) < 2:
            return 0.0
        
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        prev_short = short_ma.iloc[-2]
        prev_long = long_ma.iloc[-2]
        
        # Golden cross / Death cross
        if current_short > current_long and prev_short <= prev_long:
            return 1.0  # Golden cross - bullish
        elif current_short < current_long and prev_short >= prev_long:
            return -1.0  # Death cross - bearish
        elif current_short > current_long:
            return 0.5  # Short MA above long MA
        elif current_short < current_long:
            return -0.5  # Short MA below long MA
        else:
            return 0.0
    
    def _make_decision(
        self, 
        ticker: str, 
        signals: Dict[str, float], 
        portfolio: Dict[str, Any], 
        current_price: float
    ) -> Dict[str, Any]:
        """Make trading decision based on combined signals."""
        
        # Combine all signals
        total_signal = sum(signals.values())
        
        # Get current position
        current_position = portfolio["positions"][ticker]["long"] - portfolio["positions"][ticker]["short"]
        
        # Position sizing configuration
        max_position_pct = self.rules_config["position_sizing"]["max_position_pct"]
        portfolio_value = portfolio["cash"] + sum(
            (pos["long"] - pos["short"]) * current_price 
            for pos in portfolio["positions"].values()
        )
        max_position_value = portfolio_value * max_position_pct
        max_shares = int(max_position_value / current_price)
        
        # Decision thresholds
        buy_threshold = 0.6
        sell_threshold = -0.6
        
        if total_signal > buy_threshold and current_position < max_shares:
            # Buy signal
            quantity = min(max_shares - current_position, max_shares // 2)
            return {"action": "buy", "quantity": quantity}
        
        elif total_signal < sell_threshold and current_position > 0:
            # Sell signal
            quantity = min(current_position, max_shares // 2)
            return {"action": "sell", "quantity": quantity}
        
        elif total_signal < sell_threshold and current_position <= 0:
            # Short signal (if not already short)
            short_position = portfolio["positions"][ticker]["short"]
            if short_position < max_shares:
                quantity = min(max_shares - short_position, max_shares // 2)
                return {"action": "short", "quantity": quantity}
        
        elif total_signal > buy_threshold and current_position < 0:
            # Cover short signal
            short_position = portfolio["positions"][ticker]["short"]
            quantity = min(short_position, max_shares // 2)
            return {"action": "cover", "quantity": quantity}
        
        # Hold if no clear signal
        return {"action": "hold", "quantity": 0}
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about the rule-based strategy."""
        return {
            "name": self.name,
            "type": "rule",
            "description": "Rule-based trading strategy using technical indicators",
            "indicators": [
                f"MACD ({self.rules_config['macd']['fast_period']}, {self.rules_config['macd']['slow_period']}, {self.rules_config['macd']['signal_period']})",
                f"RSI ({self.rules_config['rsi']['period']})",
                f"Moving Average ({self.rules_config['moving_average']['short_period']}, {self.rules_config['moving_average']['long_period']})"
            ],
            "config": self.rules_config
        }
