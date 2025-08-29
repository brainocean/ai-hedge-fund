"""
AI-based trading strategy using LLM agents.
"""
from typing import Dict, List, Any
from app.backend.services.strategies.strategy import TradingStrategy
from app.backend.services.graph import run_graph_async, parse_hedge_fund_response
from app.backend.services.portfolio import create_portfolio


class AiStrategy(TradingStrategy):
    """
    AI-based trading strategy that uses LLM agents for decision making.
    """
    
    def __init__(self, graph, model_name: str = "gpt-4.1", model_provider: str = "OpenAI"):
        super().__init__("AI Strategy")
        self.graph = graph
        self.model_name = model_name
        self.model_provider = model_provider
    
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
        Generate trading signals using AI agents.
        """
        try:
            # Create portfolio for this iteration
            portfolio_for_graph = create_portfolio(
                initial_cash=portfolio["cash"],
                margin_requirement=portfolio["margin_requirement"],
                tickers=tickers,
                portfolio_positions=[]  # We'll handle positions manually
            )
            
            # Copy current portfolio state to the graph portfolio
            portfolio_for_graph.update(portfolio)

            # Execute graph-based agent decisions
            result = await run_graph_async(
                graph=self.graph,
                portfolio=portfolio_for_graph,
                tickers=tickers,
                start_date=lookback_start,
                end_date=current_date,
                model_name=self.model_name,
                model_provider=self.model_provider,
                request=request,
            )
            
            # Parse the decisions from the graph result
            if result and result.get("messages"):
                decisions = parse_hedge_fund_response(result["messages"][-1].content)
                analyst_signals = result.get("data", {}).get("analyst_signals", {})
            else:
                decisions = {}
                analyst_signals = {}
                
            # Ensure all tickers have decisions
            for ticker in tickers:
                if ticker not in decisions:
                    decisions[ticker] = {"action": "hold", "quantity": 0}
                    
            return decisions
            
        except Exception as e:
            print(f"Error in AI strategy for {current_date}: {e}")
            # Return hold decisions for all tickers on error
            return {ticker: {"action": "hold", "quantity": 0} for ticker in tickers}
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """
        Get information about the AI strategy.
        """
        return {
            "name": self.name,
            "type": "ai",
            "model_name": self.model_name,
            "model_provider": self.model_provider,
            "description": "AI-based trading strategy using LLM agents for decision making",
            "features": [
                "Multi-agent analysis",
                "Sentiment analysis",
                "Technical analysis",
                "Fundamental analysis",
                "Risk management"
            ]
        }
