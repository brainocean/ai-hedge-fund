"""
Configuration settings for the AI hedge fund application.
"""
import os
from typing import Dict, Any


class Config:
    """Application configuration."""
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///hedge_fund.db")
    
    # Trading strategy settings
    STRATEGY_TYPE = os.getenv("STRATEGY_TYPE", "ai")  # "ai" or "rule"
    
    # AI Strategy settings
    DEFAULT_MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-4.1")
    DEFAULT_MODEL_PROVIDER = os.getenv("DEFAULT_MODEL_PROVIDER", "OpenAI")
    
    # Rule Strategy settings
    RULE_STRATEGY_CONFIG = {
        "macd": {
            "enabled": os.getenv("MACD_ENABLED", "true").lower() == "true",
            "fast_period": int(os.getenv("MACD_FAST_PERIOD", "12")),
            "slow_period": int(os.getenv("MACD_SLOW_PERIOD", "26")),
            "signal_period": int(os.getenv("MACD_SIGNAL_PERIOD", "9")),
            "weight": float(os.getenv("MACD_WEIGHT", "0.4"))
        },
        "rsi": {
            "enabled": os.getenv("RSI_ENABLED", "true").lower() == "true",
            "period": int(os.getenv("RSI_PERIOD", "14")),
            "overbought": float(os.getenv("RSI_OVERBOUGHT", "70")),
            "oversold": float(os.getenv("RSI_OVERSOLD", "30")),
            "weight": float(os.getenv("RSI_WEIGHT", "0.3"))
        },
        "moving_average": {
            "enabled": os.getenv("MA_ENABLED", "true").lower() == "true",
            "short_period": int(os.getenv("MA_SHORT_PERIOD", "20")),
            "long_period": int(os.getenv("MA_LONG_PERIOD", "50")),
            "weight": float(os.getenv("MA_WEIGHT", "0.3"))
        },
        "position_sizing": {
            "max_position_pct": float(os.getenv("MAX_POSITION_PCT", "0.1")),
            "risk_per_trade": float(os.getenv("RISK_PER_TRADE", "0.02"))
        }
    }
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    @classmethod
    def get_strategy_config(cls) -> Dict[str, Any]:
        """Get strategy configuration based on current strategy type."""
        return {
            "strategy_type": cls.STRATEGY_TYPE,
            "ai_config": {
                "model_name": cls.DEFAULT_MODEL_NAME,
                "model_provider": cls.DEFAULT_MODEL_PROVIDER
            },
            "rule_config": cls.RULE_STRATEGY_CONFIG
        }
