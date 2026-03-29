from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ProductionDailyData(BaseModel):
    """生产日报数据"""
    date: date
    planned_quantity: int = Field(description="排产数量")
    actual_output: int = Field(description="实际产出")
    capacity_achievement_rate: float = Field(description="产能达成率 (%)")
    first_pass_rate: float = Field(description="一次直通率 (%)")
    material_utilization_rate: float = Field(description="材料利用率 (%)")
    daily_human_efficiency: float = Field(description="日人效 (元/人)")
    attendance_headcount: int = Field(description="出勤人头")
    total_labor_cost: float = Field(description="总工费额 (元)")
    gross_profit: float = Field(description="毛利额 (元)")
    gross_profit_rate: float = Field(description="毛利率 (%)")
    material_ratio: float = Field(description="料占比 (%)")
    labor_ratio: float = Field(description="工占比 (%)")
    overhead_ratio: float = Field(description="费占比 (%)")


class ActionItem(BaseModel):
    """改善动作项"""
    action: str = Field(description="具体动作描述")
    expected_impact: str = Field(description="预期效果")
    priority: str = Field(description="优先级: 高/中/低")


class LaborEfficiencyAnalysis(BaseModel):
    """人工与效率分析"""
    findings: List[str] = Field(description="问题发现列表")
    root_causes: List[str] = Field(description="根本原因列表")
    actions: List[str] = Field(description="建议动作列表")


class QualityCostAnalysis(BaseModel):
    """质量成本分析"""
    findings: List[str] = Field(description="问题发现列表")
    root_causes: List[str] = Field(description="根本原因列表")
    actions: List[str] = Field(description="建议动作列表")


class ImprovementPlan(BaseModel):
    """改善方案"""
    priority_actions: List[ActionItem] = Field(description="优先改善动作列表")


class AnalysisResult(BaseModel):
    """智能分析结果"""
    summary: str = Field(description="成本动因总览概述")
    key_findings: List[str] = Field(description="关键发现列表")
    labor_efficiency: LaborEfficiencyAnalysis
    quality_cost: QualityCostAnalysis
    improvement_plan: ImprovementPlan


class AnalysisResponse(BaseModel):
    """API 响应"""
    code: int = 0
    message: str = "success"
    data: AnalysisResult
