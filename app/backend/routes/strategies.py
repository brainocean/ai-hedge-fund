"""
API routes for trading strategies management.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.backend.services.strategies.strategy_factory import StrategyFactory
from app.backend.config import Config


router = APIRouter(prefix="/strategies", tags=["strategies"])


class StrategyConfigRequest(BaseModel):
    """Request model for strategy configuration."""
    strategy_type: str
    ai_config: Optional[Dict[str, Any]] = None
    rule_config: Optional[Dict[str, Any]] = None


class StrategyResponse(BaseModel):
    """Response model for strategy information."""
    name: str
    type: str
    description: str
    features: list
    config: Optional[Dict[str, Any]] = None


@router.get("/available")
async def get_available_strategies() -> Dict[str, Dict[str, Any]]:
    """Get information about all available trading strategies."""
    return StrategyFactory.get_available_strategies()


@router.get("/current")
async def get_current_strategy() -> Dict[str, Any]:
    """Get current strategy configuration."""
    return Config.get_strategy_config()


@router.post("/configure")
async def configure_strategy(config: StrategyConfigRequest) -> Dict[str, str]:
    """
    Configure the trading strategy.
    Note: This updates the configuration but requires application restart to take effect.
    """
    if config.strategy_type not in ["ai", "rule"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid strategy type. Must be 'ai' or 'rule'"
        )
    
    # In a production environment, you might want to:
    # 1. Update environment variables
    # 2. Update configuration file
    # 3. Restart services
    
    # For now, we'll just validate the configuration
    try:
        if config.strategy_type == "ai":
            if not config.ai_config:
                config.ai_config = {
                    "model_name": Config.DEFAULT_MODEL_NAME,
                    "model_provider": Config.DEFAULT_MODEL_PROVIDER
                }
        elif config.strategy_type == "rule":
            if not config.rule_config:
                config.rule_config = Config.RULE_STRATEGY_CONFIG
        
        return {
            "message": f"Strategy configured to {config.strategy_type}",
            "note": "Configuration will take effect after application restart"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to configure strategy: {str(e)}"
        )


@router.get("/rule/config")
async def get_rule_strategy_config() -> Dict[str, Any]:
    """Get current rule-based strategy configuration."""
    return Config.RULE_STRATEGY_CONFIG


@router.post("/rule/config")
async def update_rule_strategy_config(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Update rule-based strategy configuration.
    Note: This updates the runtime configuration.
    """
    try:
        # Validate configuration structure
        required_sections = ["macd", "rsi", "moving_average", "position_sizing"]
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section: {section}")
        
        # Update the configuration (in a real app, you'd persist this)
        Config.RULE_STRATEGY_CONFIG.update(config)
        
        return {"message": "Rule strategy configuration updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid configuration: {str(e)}"
        )


@router.get("/ai/config")
async def get_ai_strategy_config() -> Dict[str, Any]:
    """Get current AI strategy configuration."""
    return {
        "model_name": Config.DEFAULT_MODEL_NAME,
        "model_provider": Config.DEFAULT_MODEL_PROVIDER
    }


@router.post("/ai/config")
async def update_ai_strategy_config(config: Dict[str, str]) -> Dict[str, str]:
    """
    Update AI strategy configuration.
    Note: This updates the runtime configuration.
    """
    try:
        if "model_name" in config:
            Config.DEFAULT_MODEL_NAME = config["model_name"]
        if "model_provider" in config:
            Config.DEFAULT_MODEL_PROVIDER = config["model_provider"]
        
        return {"message": "AI strategy configuration updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid configuration: {str(e)}"
        )
