# 日成本智能分析看板

基于 LLM 的量产日成本智能原因分析系统。

## 功能特性

- **智能原因分析**：基于生产数据（排产数量、产能达成率、一次直通率、毛利率等）自动分析成本动因
- **四维分析框架**：成本动因总览 → 人工与效率 → 质量成本 → 改善方案
- **多 LLM 支持**：OpenAI / DeepSeek / 智谱 AI

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 LLM_API_KEY 和 LLM_PROVIDER

# 启动服务
python main.py
```

API 文档：`http://localhost:8000/docs`

## API 接口

### POST /api/analysis/daily-cost

```json
{
  "date": "2026-03-29",
  "planned_quantity": 10000,
  "actual_output": 9200,
  "capacity_achievement_rate": 92.0,
  "first_pass_rate": 96.5,
  "material_utilization_rate": 94.2,
  "daily_human_efficiency": 1850.5,
  "attendance_headcount": 45,
  "total_labor_cost": 83250.0,
  "gross_profit": 156800.0,
  "gross_profit_rate": 18.2,
  "material_ratio": 65.5,
  "labor_ratio": 9.6,
  "overhead_ratio": 6.7
}
```

## 技术栈

- FastAPI + Pydantic + Uvicorn
- OpenAI SDK / DeepSeek API / 智谱 AI API
