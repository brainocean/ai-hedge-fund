# AI对冲基金项目概述

## 项目简介

这是一个基于AI的对冲基金概念验证项目，旨在探索使用人工智能进行交易决策。该系统采用多智能体协作的方式，模拟知名投资大师的投资策略，为教育和研究目的而设计。

## 核心架构

### 1. 系统整体架构

```mermaid
graph TB
    subgraph "用户界面层"
        UI[Web前端界面]
        CLI[命令行界面]
    end
    
    subgraph "应用服务层"
        API[FastAPI后端服务]
        ENGINE[LangGraph核心引擎]
    end
    
    subgraph "智能体层"
        AGENTS[AI智能体群]
    end
    
    subgraph "数据服务层"
        DATA[数据获取服务]
        STORAGE[数据存储服务]
    end
    
    subgraph "外部服务层"
        LLM[大语言模型服务]
        MARKET[金融数据API]
    end
    
    UI --> API
    CLI --> ENGINE
    API --> ENGINE
    ENGINE --> AGENTS
    AGENTS --> LLM
    ENGINE --> DATA
    DATA --> MARKET
    API --> STORAGE
    ENGINE --> STORAGE
    
    style UI fill:#e1f5fe
    style API fill:#f3e5f5
    style ENGINE fill:#e8f5e8
    style AGENTS fill:#fff3e0
    style DATA fill:#fce4ec
    style LLM fill:#f1f8e9
    style STORAGE fill:#e0f2f1
```

### 2. 前端架构详图

```mermaid
graph TB
    subgraph "React前端应用"
        APP[App.tsx 主应用]
        
        subgraph "核心组件"
            FLOW[Flow.tsx 流程编辑器]
            LAYOUT[Layout.tsx 布局管理]
            CONTROLS[CustomControls.tsx 控制组件]
        end
        
        subgraph "上下文管理"
            FC[FlowContext 流程上下文]
            LC[LayoutContext 布局上下文]
            NC[NodeContext 节点上下文]
            TC[TabsContext 标签上下文]
        end
        
        subgraph "业务组件"
            PANELS[面板组件]
            SETTINGS[设置组件]
            TABS[标签组件]
            NODES[节点组件]
        end
        
        subgraph "服务层"
            API_SERVICE[API服务]
            WEBSOCKET[WebSocket服务]
        end
    end
    
    APP --> FLOW
    APP --> LAYOUT
    FLOW --> CONTROLS
    FLOW --> FC
    LAYOUT --> LC
    FC --> NC
    LC --> TC
    FLOW --> PANELS
    PANELS --> SETTINGS
    SETTINGS --> TABS
    TABS --> NODES
    API_SERVICE --> WEBSOCKET
    
    style APP fill:#e1f5fe
    style FLOW fill:#f0f4ff
    style FC fill:#e8f5e8
    style API_SERVICE fill:#fff3e0
```

### 3. 后端架构详图

```mermaid
graph TB
    subgraph "FastAPI后端服务"
        MAIN[main.py 应用入口]
        
        subgraph "路由层"
            ROUTES[API路由集合]
            HEALTH[健康检查]
            FLOWS[流程管理]
            RUNS[运行管理]
            KEYS[密钥管理]
            STRATEGIES[策略管理]
        end
        
        subgraph "服务层"
            AGENT_SVC[智能体服务]
            BACKTEST_SVC[回测服务]
            OLLAMA_SVC[Ollama服务]
            KEY_SVC[密钥服务]
        end
        
        subgraph "数据层"
            MODELS[数据模型]
            REPOS[数据仓库]
            DB[数据库连接]
        end
        
        subgraph "外部集成"
            GRAPH_SVC[图服务]
            PORTFOLIO_SVC[投资组合服务]
        end
    end
    
    MAIN --> ROUTES
    ROUTES --> HEALTH
    ROUTES --> FLOWS
    ROUTES --> RUNS
    ROUTES --> KEYS
    ROUTES --> STRATEGIES
    
    FLOWS --> AGENT_SVC
    RUNS --> BACKTEST_SVC
    KEYS --> KEY_SVC
    STRATEGIES --> OLLAMA_SVC
    
    AGENT_SVC --> MODELS
    BACKTEST_SVC --> REPOS
    KEY_SVC --> DB
    
    AGENT_SVC --> GRAPH_SVC
    BACKTEST_SVC --> PORTFOLIO_SVC
    
    style MAIN fill:#f3e5f5
    style ROUTES fill:#e8f5e8
    style AGENT_SVC fill:#fff3e0
    style MODELS fill:#e0f2f1
```

### 4. 智能体架构详图

```mermaid
graph TB
    subgraph "智能体生态系统"
        subgraph "投资大师智能体"
            BUFFETT[Warren Buffett<br/>价值投资]
            MUNGER[Charlie Munger<br/>理性投资]
            BURRY[Michael Burry<br/>逆向投资]
            WOOD[Cathie Wood<br/>成长投资]
            ACKMAN[Bill Ackman<br/>激进投资]
            GRAHAM[Ben Graham<br/>价值投资鼻祖]
            FISHER[Phil Fisher<br/>成长投资]
            LYNCH[Peter Lynch<br/>实用投资]
            OTHERS[其他投资大师...]
        end
        
        subgraph "专业分析智能体"
            FUNDAMENTAL[基本面分析<br/>财务数据分析]
            TECHNICAL[技术分析<br/>图表模式识别]
            SENTIMENT[情感分析<br/>市场情绪评估]
            VALUATION[估值分析<br/>内在价值计算]
        end
        
        subgraph "管理智能体"
            RISK[风险管理<br/>风险评估与控制]
            PORTFOLIO[投资组合管理<br/>最终交易决策]
        end
        
        subgraph "支撑服务"
            STATE[状态管理]
            MESSAGE[消息传递]
            WORKFLOW[工作流编排]
        end
    end
    
    BUFFETT --> RISK
    MUNGER --> RISK
    BURRY --> RISK
    WOOD --> RISK
    ACKMAN --> RISK
    GRAHAM --> RISK
    FISHER --> RISK
    LYNCH --> RISK
    OTHERS --> RISK
    
    FUNDAMENTAL --> RISK
    TECHNICAL --> RISK
    SENTIMENT --> RISK
    VALUATION --> RISK
    
    RISK --> PORTFOLIO
    
    STATE --> WORKFLOW
    MESSAGE --> WORKFLOW
    WORKFLOW --> BUFFETT
    WORKFLOW --> FUNDAMENTAL
    WORKFLOW --> RISK
    
    style BUFFETT fill:#e3f2fd
    style FUNDAMENTAL fill:#f1f8e9
    style RISK fill:#fce4ec
    style STATE fill:#e8f5e8
```

### 5. 数据架构详图

```mermaid
graph TB
    subgraph "数据管理系统"
        subgraph "数据获取层"
            API_CLIENT[金融数据API客户端]
            CACHE[数据缓存系统]
            VALIDATOR[数据验证器]
        end
        
        subgraph "数据处理层"
            PROCESSOR[数据处理器]
            TRANSFORMER[数据转换器]
            AGGREGATOR[数据聚合器]
        end
        
        subgraph "数据存储层"
            SQLITE[SQLite数据库]
            FLOW_TABLE[流程配置表]
            RUN_TABLE[运行记录表]
            CYCLE_TABLE[分析周期表]
            KEY_TABLE[API密钥表]
        end
        
        subgraph "数据模型层"
            AGENT_STATE[智能体状态模型]
            PORTFOLIO[投资组合模型]
            MARKET_DATA[市场数据模型]
            SIGNAL[交易信号模型]
        end
        
        subgraph "外部数据源"
            FINANCIAL_API[金融数据API]
            MARKET_FEED[市场数据源]
            NEWS_API[新闻数据API]
        end
    end
    
    FINANCIAL_API --> API_CLIENT
    MARKET_FEED --> API_CLIENT
    NEWS_API --> API_CLIENT
    
    API_CLIENT --> CACHE
    CACHE --> VALIDATOR
    VALIDATOR --> PROCESSOR
    
    PROCESSOR --> TRANSFORMER
    TRANSFORMER --> AGGREGATOR
    AGGREGATOR --> AGENT_STATE
    
    AGENT_STATE --> PORTFOLIO
    PORTFOLIO --> MARKET_DATA
    MARKET_DATA --> SIGNAL
    
    SIGNAL --> SQLITE
    SQLITE --> FLOW_TABLE
    SQLITE --> RUN_TABLE
    SQLITE --> CYCLE_TABLE
    SQLITE --> KEY_TABLE
    
    style API_CLIENT fill:#e3f2fd
    style PROCESSOR fill:#f1f8e9
    style SQLITE fill:#e0f2f1
    style AGENT_STATE fill:#fff3e0
    style FINANCIAL_API fill:#fce4ec
```

## 主要模块功能

### 1. 前端模块 (app/frontend/)
- **技术栈**: React + TypeScript + Vite
- **主要功能**:
  - 可视化流程设计器，支持拖拽式构建投资策略
  - 实时监控投资组合表现
  - 智能体配置和参数调整
  - 回测结果可视化

### 2. 后端API模块 (app/backend/)
- **技术栈**: FastAPI + SQLAlchemy + Alembic
- **主要功能**:
  - RESTful API服务
  - 数据库管理和迁移
  - 流程执行管理
  - API密钥管理

### 3. 核心引擎模块 (src/)
- **技术栈**: LangGraph + LangChain
- **主要功能**:
  - 智能体工作流编排
  - 状态管理和消息传递
  - 策略执行引擎
  - 回测系统

### 4. 智能体模块 (src/agents/)
包含18个专业投资智能体：

#### 投资大师智能体
- **Warren Buffett**: 价值投资，寻找优秀公司
- **Charlie Munger**: 理性投资，避免愚蠢决策
- **Michael Burry**: 逆向投资，寻找深度价值
- **Cathie Wood**: 成长投资，专注创新颠覆
- **Bill Ackman**: 激进投资，推动企业变革
- **其他大师**: Ben Graham, Phil Fisher, Peter Lynch等

#### 专业分析智能体
- **基本面分析**: 财务数据分析
- **技术分析**: 图表模式识别
- **情感分析**: 市场情绪评估
- **估值分析**: 内在价值计算

#### 管理智能体
- **风险管理**: 风险评估和头寸限制
- **投资组合管理**: 最终交易决策

### 5. 数据模块 (src/data/, src/tools/)
- **数据获取**: 金融数据API集成
- **数据缓存**: 提高性能和降低成本
- **数据模型**: 标准化数据结构

### 6. LLM模块 (src/llm/)
- **多模型支持**: OpenAI, Anthropic, Groq, Ollama
- **模型管理**: 动态模型选择和配置
- **成本优化**: 智能模型路由

## 数据流图

```mermaid
flowchart TD
    subgraph "数据输入"
        A1[股票代码列表]
        A2[时间范围]
        A3[初始投资组合]
        A4[模型配置]
    end
    
    subgraph "数据获取层"
        B1[金融数据API]
        B2[市场数据缓存]
        B3[历史价格数据]
        B4[基本面数据]
        B5[技术指标数据]
    end
    
    subgraph "智能体分析层"
        C1[投资大师智能体群]
        C2[专业分析智能体群]
        C3[LLM推理引擎]
    end
    
    subgraph "决策聚合层"
        D1[风险管理评估]
        D2[投资组合优化]
        D3[交易信号生成]
    end
    
    subgraph "执行层"
        E1[模拟交易执行]
        E2[投资组合更新]
        E3[绩效计算]
    end
    
    subgraph "输出结果"
        F1[交易决策]
        F2[投资组合状态]
        F3[绩效指标]
        F4[智能体推理过程]
    end
    
    subgraph "持久化存储"
        G1[流程配置]
        G2[运行历史]
        G3[分析周期]
        G4[绩效记录]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> D2
    A4 --> C3
    
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B1 --> B5
    
    B2 --> C1
    B3 --> C1
    B4 --> C2
    B5 --> C2
    
    C1 --> C3
    C2 --> C3
    C3 --> D1
    
    D1 --> D2
    D2 --> D3
    D3 --> E1
    
    E1 --> E2
    E2 --> E3
    E3 --> F1
    
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    F1 --> G2
    F2 --> G3
    F3 --> G4
    E2 --> G1
    
    style A1 fill:#e3f2fd
    style B1 fill:#f1f8e9
    style C1 fill:#fff3e0
    style D1 fill:#fce4ec
    style E1 fill:#e8f5e8
    style F1 fill:#f3e5f5
    style G1 fill:#e0f2f1
```

## 核心数据实体

### 1. AgentState (智能体状态)
```python
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]  # 消息序列
    data: dict[str, any]            # 共享数据
    metadata: dict[str, any]        # 元数据
```

### 2. Portfolio (投资组合)
```python
portfolio = {
    "cash": float,                  # 现金余额
    "margin_requirement": float,    # 保证金要求
    "positions": {                  # 持仓信息
        ticker: {
            "long": int,            # 多头股数
            "short": int,           # 空头股数
            "long_cost_basis": float,   # 多头成本基础
            "short_cost_basis": float,  # 空头成本基础
        }
    },
    "realized_gains": dict          # 已实现收益
}
```

### 3. HedgeFundFlow (流程配置)
- 存储React Flow的节点和边配置
- 包含智能体选择和参数设置
- 支持模板化和标签分类

### 4. HedgeFundFlowRun (运行记录)
- 跟踪每次执行的完整生命周期
- 记录初始和最终投资组合状态
- 存储错误信息和绩效指标

### 5. HedgeFundFlowRunCycle (分析周期)
- 记录每个分析周期的详细信息
- 包含所有智能体的信号和决策
- 跟踪API调用成本和性能指标

## 工作流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端API
    participant E as 核心引擎
    participant A as 智能体群
    participant D as 数据源
    participant L as LLM模型
    
    U->>F: 配置投资策略
    F->>B: 提交流程配置
    B->>E: 启动工作流
    
    loop 智能体分析
        E->>D: 获取市场数据
        D-->>E: 返回数据
        E->>A: 分发数据给智能体
        A->>L: 调用LLM推理
        L-->>A: 返回分析结果
        A-->>E: 返回投资信号
    end
    
    E->>A: 风险管理评估
    A-->>E: 风险评估结果
    E->>A: 投资组合管理
    A-->>E: 最终交易决策
    
    E->>B: 返回执行结果
    B->>F: 推送结果更新
    F->>U: 显示投资决策
```

## 技术特点

### 1. 模块化设计
- 前后端分离架构
- 智能体可插拔设计
- 多模型支持

### 2. 可扩展性
- 支持自定义智能体
- 灵活的工作流配置
- 多种LLM模型集成

### 3. 实时性
- WebSocket实时通信
- 流式数据处理
- 增量状态更新

### 4. 可观测性
- 详细的执行日志
- 智能体推理过程可视化
- 绩效指标跟踪

### 5. 成本控制
- API调用计数
- 模型成本估算
- 缓存机制优化

## 部署方式

### 1. 命令行模式
- 直接运行Python脚本
- 适合批量处理和自动化
- 支持Docker容器化

### 2. Web应用模式
- 全栈Web应用
- 可视化界面操作
- 实时监控和管理

### 3. 混合模式
- Web界面配置策略
- 命令行执行回测
- 灵活的部署选择

## 安全考虑

- API密钥加密存储
- 环境变量配置
- 数据库访问控制
- CORS跨域保护

## 未来扩展

- 实盘交易接口集成
- 更多投资大师智能体
- 高级风险管理策略
- 机器学习模型集成
- 云端部署支持

---

*注意：本项目仅用于教育和研究目的，不构成投资建议。*
