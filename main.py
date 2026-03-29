from fastapi import FastAPI
from pydantic import ValidationError
from models import ProductionDailyData, AnalysisResponse
from analysis_service import analyze_production_data

app = FastAPI(title="日成本智能分析 API", version="1.0.0")


@app.post("/api/analysis/daily-cost", response_model=AnalysisResponse)
async def analyze_daily_cost(data: ProductionDailyData):
    """
    智能分析日成本数据

    输入生产日报数据，返回包含成本动因总览、人工效率分析、
    质量成本分析和改善方案的完整分析结果。
    """
    try:
        result = await analyze_production_data(data)
        return AnalysisResponse(code=0, message="success", data=result)
    except ValidationError as e:
        return AnalysisResponse(code=1, message=f"数据验证错误: {str(e)}", data=None)
    except Exception as e:
        return AnalysisResponse(code=2, message=f"分析失败: {str(e)}", data=None)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
