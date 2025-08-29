# AI Hedge Fund - 技术上下文

## 技术栈

### 后端技术
- **Python 3.8+**: 主要编程语言
- **LangGraph**: 多智能体工作流管理
- **LangChain**: LLM集成和提示管理
- **FastAPI**: Web API框架
- **SQLAlchemy**: 数据库ORM
- **Alembic**: 数据库迁移工具
- **Pydantic**: 数据验证和序列化

### 前端技术
- **React 18**: 前端框架
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 构建工具和开发服务器
- **Tailwind CSS**: 样式框架
- **React Flow**: 流程图可视化
- **Shadcn/ui**: UI组件库

### 数据和存储
- **SQLite**: 本地数据库（开发环境）
- **PostgreSQL**: 生产数据库（可选）
- **Redis**: 缓存系统（可选）
- **Financial Datasets API**: 股票数据源

### LLM集成
- **OpenAI API**: GPT-4, GPT-4o, GPT-4o-mini
- **Groq API**: Llama3, DeepSeek等模型
- **Anthropic API**: Claude系列模型
- **Ollama**: 本地LLM运行
- **DeepSeek API**: DeepSeek模型

## 开发环境

### 依赖管理
```toml
# pyproject.toml - Poetry配置
[tool.poetry]
name = "ai-hedge-fund"
version = "0.1.0"
description = "AI-powered hedge fund for educational purposes"

[tool.poetry.dependencies]
python = "^3.8"
langchain = "^0.1.0"
langgraph = "^0.0.40"
fastapi = "^0.104.0"
# ... 其他依赖
```

### 环境配置
```bash
# .env 文件结构
OPENAI_API_KEY=your-openai-api-key
GROQ_API_KEY=your-groq-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# 数据库配置
DATABASE_URL=sqlite:///./hedge_fund.db

# 应用配置
DEBUG=true
LOG_LEVEL=INFO
```

## 项目结构

### 核心目录结构
```
ai-hedge-fund/
├── src/                    # 核心Python代码
│   ├── agents/            # 智能体实现
│   ├── data/              # 数据模型和缓存
│   ├── graph/             # LangGraph状态管理
│   ├── llm/               # LLM配置和管理
│   ├── tools/             # 工具函数
│   └── utils/             # 通用工具
├── app/                   # Web应用
│   ├── backend/           # FastAPI后端
│   └── frontend/          # React前端
├── docs/                  # 文档
├── tests/                 # 测试代码
├── memory-bank/           # 内存银行
└── docker/                # Docker配置
```

### 关键文件
- `src/main.py`: CLI入口点
- `src/backtester.py`: 回测系统
- `app/backend/main.py`: Web API入口
- `app/frontend/src/App.tsx`: 前端主组件

## 开发工具链

### 代码质量
- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查
- **pytest**: 单元测试

### 前端工具
- **ESLint**: JavaScript/TypeScript代码检查
- **Prettier**: 代码格式化
- **TypeScript**: 类型检查

### 构建和部署
- **Poetry**: Python依赖管理
- **Docker**: 容器化部署
- **Docker Compose**: 多服务编排

## API集成

### Financial Datasets API
```python
# 数据获取模式
class FinancialDataAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
    
    def get_stock_data(self, ticker: str, period: str) -> dict:
        # 获取股票数据
        pass
```

### LLM API集成
```python
# LLM配置模式
LLM_CONFIGS = {
    "openai": {
        "gpt-4o": {"max_tokens": 4096, "temperature": 0.1},
        "gpt-4o-mini": {"max_tokens": 2048, "temperature": 0.1}
    },
    "groq": {
        "llama3-70b": {"max_tokens": 8192, "temperature": 0.1}
    }
}
```

## 数据库设计

### 核心表结构
```sql
-- 对冲基金流程表
CREATE TABLE hedge_fund_flows (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 流程运行表
CREATE TABLE hedge_fund_flow_runs (
    id INTEGER PRIMARY KEY,
    flow_id INTEGER REFERENCES hedge_fund_flows(id),
    status VARCHAR(50),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- API密钥管理表
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    encrypted_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 性能考虑

### 缓存策略
- **内存缓存**: 频繁访问的数据
- **文件缓存**: 股票数据缓存
- **Redis缓存**: 分布式缓存（可选）

### 并发处理
- **异步IO**: FastAPI异步处理
- **线程池**: CPU密集型任务
- **连接池**: 数据库连接管理

### 资源优化
- **LLM调用限制**: 避免过度调用
- **数据分页**: 大数据集分页处理
- **内存管理**: 及时释放不需要的对象

## 安全考虑

### API密钥管理
- **环境变量**: 敏感信息不硬编码
- **加密存储**: 数据库中的密钥加密
- **访问控制**: API访问权限控制

### 数据安全
- **输入验证**: 所有用户输入验证
- **SQL注入防护**: 使用ORM防止注入
- **CORS配置**: 跨域请求安全配置

## 部署配置

### Docker配置
```dockerfile
# Dockerfile示例
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.backend.main:app", "--host", "0.0.0.0"]
```

### 环境部署
- **开发环境**: 本地SQLite + 本地LLM
- **测试环境**: Docker + 云端LLM
- **生产环境**: Kubernetes + PostgreSQL + Redis

## 监控和日志

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hedge_fund.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控
- **响应时间**: API响应时间监控
- **错误率**: 错误发生率统计
- **资源使用**: CPU、内存使用监控
- **LLM调用**: API调用次数和成本监控

## 测试策略

### 单元测试
- **智能体测试**: 每个智能体的独立测试
- **API测试**: FastAPI端点测试
- **数据层测试**: 数据库操作测试

### 集成测试
- **端到端测试**: 完整流程测试
- **API集成测试**: 外部API集成测试
- **前后端集成**: 前后端交互测试

### 性能测试
- **负载测试**: 高并发场景测试
- **压力测试**: 系统极限测试
- **内存泄漏测试**: 长时间运行测试
