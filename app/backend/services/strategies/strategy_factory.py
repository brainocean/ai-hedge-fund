"""
Factory for creating trading strategies.
"""
from typing import Dict, Any, Optional
from app.backend.services.strategies.strategy import TradingStrategy
from app.backend.services.strategies.ai_strategy import AiStrategy
from app.backend.services.strategies.rule_strategy import RuleStrategy
from app.backend.config import Config


class StrategyFactory:
    """Factory for creating trading strategies."""
    
    @staticmethod
    def create_strategy(
        strategy_type: str = None,
        graph=None,
        model_name: str = None,
        model_provider: str = None,
        rules_config: Dict[str, Any] = None
    ) -> TradingStrategy:
        """
        Create a trading strategy based on the specified type.
        
        Args:
            strategy_type: Type of strategy ("ai" or "rule")
            graph: Pre-compiled graph for AI strategy
            model_name: Model name for AI strategy
            model_provider: Model provider for AI strategy
            rules_config: Configuration for rule-based strategy
            
        Returns:
            TradingStrategy instance
        """
        # Use config defaults if not specified
        if strategy_type is None:
            strategy_type = Config.STRATEGY_TYPE
        
        if strategy_type == "ai":
            if model_name is None:
                model_name = Config.DEFAULT_MODEL_NAME
            if model_provider is None:
                model_provider = Config.DEFAULT_MODEL_PROVIDER
                
            if graph is None:
                raise ValueError("Graph is required for AI strategy")
                
            return AiStrategy(
                graph=graph,
                model_name=model_name,
                model_provider=model_provider
            )
        
        elif strategy_type == "rule":
            if rules_config is None:
                rules_config = Config.RULE_STRATEGY_CONFIG
                
            return RuleStrategy(rules_config=rules_config)
        
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
    
    @staticmethod
    def get_available_strategies() -> Dict[str, Dict[str, Any]]:
        """Get information about available strategies."""
        return {
            "ai": {
                "name": "AI Strategy",
                "description": "AI-based trading strategy using LLM agents",
                "type": "ai",
                "features": [
                    "Multi-agent analysis",
                    "Sentiment analysis", 
                    "Technical analysis",
                    "Fundamental analysis",
                    "Risk management"
                ]
            },
            "rule": {
                "name": "Rule Strategy",
                "description": "Rule-based trading strategy using technical indicators",
                "type": "rule",
                "features": [
                    "MACD signals",
                    "RSI analysis",
                    "Moving average crossovers",
                    "Position sizing rules",
                    "Risk management"
                ]
            }
        }
