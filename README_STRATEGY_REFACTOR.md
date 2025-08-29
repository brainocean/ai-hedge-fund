# 交易策略重构完成指南

## 概述

本项目已成功重构为支持AI策略与自定义规则策略（如MACD）之间的灵活切换。通过策略模式（Strategy Pattern）实现了统一的交易决策接口。

## 新增文件结构

```
app/backend/
├── config.py                          # 配置管理，支持环境变量
├── services/strategies/                # 策略模块
│   ├── __init__.py
│   ├── strategy.py                     # 策略基类接口
│   ├── ai_strategy.py                  # AI策略实现
│   ├── rule_strategy.py                # 规则策略实现（MACD、RSI、MA）
│   └── strategy_factory.py             # 策略工厂
└── routes/strategies.py                # 策略管理API路由
```

## 核心功能

### 1. 策略接口 (`TradingStrategy`)
- 统一的 `generate_signals()` 方法
- 异步支持
- 标准化的输入输出格式

### 2. AI策略 (`AiStrategy`)
- 封装现有的LLM+Graph决策逻辑
- 保持与原有系统的兼容性
- 支持多代理分析

### 3. 规则策略 (`RuleStrategy`)
- MACD信号生成
- RSI超买超卖检测
- 移动平均线交叉
- 可配置的权重和参数
- 智能仓位管理

### 4. 配置管理
- 环境变量支持
- 运行时配置更新
- 策略参数调优

## 使用方法

### 环境变量配置

```bash
# 策略类型选择
STRATEGY_TYPE=rule  # 或 "ai"

# 规则策略参数
MACD_ENABLED=true
MACD_FAST_PERIOD=12
MACD_SLOW_PERIOD=26
MACD_SIGNAL_PERIOD=9
MACD_WEIGHT=0.4

RSI_ENABLED=true
RSI_PERIOD=14
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
RSI_WEIGHT=0.3

MA_ENABLED=true
MA_SHORT_PERIOD=20
MA_LONG_PERIOD=50
MA_WEIGHT=0.3

MAX_POSITION_PCT=0.1
RISK_PER_TRADE=0.02
```

### API接口

#### 获取可用策略
```http
GET /strategies/available
```

#### 获取当前策略配置
```http
GET /strategies/current
```

#### 切换策略
```http
POST /strategies/configure
Content-Type: application/json

{
  "strategy_type": "rule",
  "rule_config": {
    "macd": {
      "enabled": true,
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9,
      "weight": 0.4
    }
  }
}
```

#### 更新规则策略配置
```http
POST /strategies/rule/config
Content-Type: application/json

{
  "macd": {
    "enabled": true,
    "fast_period": 10,
    "slow_period": 21,
    "signal_period": 9,
    "weight": 0.5
  }
}
```

### 代码使用示例

```python
from app.backend.services.strategies.strategy_factory import StrategyFactory
from app.backend.services.backtest_service import BacktestService

# 创建规则策略
strategy = StrategyFactory.create_strategy(
    strategy_type="rule",
    rules_config={
        "macd": {"enabled": True, "fast_period": 12, "slow_period": 26},
        "rsi": {"enabled": True, "period": 14},
        "moving_average": {"enabled": True, "short_period": 20, "long_period": 50}
    }
)

# 在回测中使用
backtest_service = BacktestService(
    portfolio=portfolio,
    tickers=["AAPL", "GOOGL"],
    start_date="2023-01-01",
    end_date="2023-12-31",
    initial_capital=100000,
    strategy=strategy
)

results = await backtest_service.run_backtest_async()
```

## 技术指标说明

### MACD (Moving Average Convergence Divergence)
- **快线周期**: 默认12天
- **慢线周期**: 默认26天
- **信号线周期**: 默认9天
- **信号逻辑**: 
  - MACD线上穿信号线 → 买入信号
  - MACD线下穿信号线 → 卖出信号

### RSI (Relative Strength Index)
- **周期**: 默认14天
- **超买阈值**: 默认70
- **超卖阈值**: 默认30
- **信号逻辑**:
  - RSI < 30 → 超卖，买入信号
  - RSI > 70 → 超买，卖出信号

### 移动平均线交叉
- **短期均线**: 默认20天
- **长期均线**: 默认50天
- **信号逻辑**:
  - 短期均线上穿长期均线 → 黄金交叉，买入信号
  - 短期均线下穿长期均线 → 死亡交叉，卖出信号

## 仓位管理

- **最大单个持仓**: 默认投资组合的10%
- **单笔交易风险**: 默认2%
- **支持多空操作**: 买入、卖出、做空、平仓

## 扩展指南

### 添加新的技术指标

1. 在 `RuleStrategy` 类中添加新的计算方法:
```python
def _calculate_bollinger_bands_signal(self, price_data: pd.DataFrame) -> float:
    # 实现布林带信号逻辑
    pass
```

2. 在配置中添加相应参数:
```python
"bollinger_bands": {
    "enabled": True,
    "period": 20,
    "std_dev": 2,
    "weight": 0.2
}
```

3. 在 `_calculate_signals` 方法中集成新指标

### 创建新的策略类型

1. 继承 `TradingStrategy` 基类
2. 实现 `generate_signals` 方法
3. 在 `StrategyFactory` 中注册新策略

## 注意事项

1. **向后兼容**: 现有的AI策略功能完全保留
2. **配置持久化**: 当前配置更新需要重启应用生效
3. **数据依赖**: 规则策略需要足够的历史数据（建议至少50个交易日）
4. **性能考虑**: 规则策略计算速度比AI策略快，适合高频回测

## 测试建议

1. 使用小资金量测试规则策略
2. 对比AI策略与规则策略的回测结果
3. 调整技术指标参数以优化表现
4. 监控实盘交易中的策略切换

通过这次重构，您现在可以：
- 在AI智能分析与传统技术分析之间自由切换
- 根据市场条件选择最适合的策略
- 通过API动态调整策略参数
- 扩展更多自定义交易规则
