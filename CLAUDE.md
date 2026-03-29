# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and set LLM_API_KEY

# Run the server
python main.py

# Run with uvicorn directly
uvicorn main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs` (Swagger UI).

## Architecture

**日成本智能分析 API** - A FastAPI service that uses LLMs to analyze manufacturing production cost data.

### Data Flow
```
ProductionDailyData (Pydantic model)
    ↓ build_user_prompt()
User prompt with structured data
    ↓ call_llm() → LLM API (OpenAI/DeepSeek/Zhipu)
Raw LLM response text
    ↓ parse_llm_response()
JSON dict
    ↓ AnalysisResult(**result_dict)
Structured AnalysisResult
```

### Core Modules
- `models.py` - Pydantic models: `ProductionDailyData` (input), `AnalysisResult` (output)
- `analysis_service.py` - `SYSTEM_PROMPT` defines the analysis logic, `analyze_production_data()` is the main entry point
- `config.py` - LLM provider config via environment variables (`LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`, `LLM_BASE_URL`)
- `main.py` - FastAPI app with single endpoint `POST /api/analysis/daily-cost`

### Adding a New LLM Provider
Add a new `call_{provider}()` function in `analysis_service.py` and update the `call_llm()` dispatcher. No other changes needed.

### Analysis Dimensions (defined in SYSTEM_PROMPT)
1. 成本动因总览 - Cost structure overview (material/labor/overhead ratios, gross profit anomalies)
2. 人工与效率动因 - Labor efficiency (capacity achievement, daily efficiency, headcount)
3. 质量成本动因 - Quality cost (first pass rate, material utilization impact)
4. 改善方案 - Improvement actions with priority and expected impact
