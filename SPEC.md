# 量产日成本看板 - 智能原因分析模块

## 1. 概述

基于生产结构化数据，使用 LLM 进行智能原因分析，输出可落地的改善方案。

## 2. 数据模型

### 2.1 生产日报数据 (ProductionDailyData)

| 字段 | 类型 | 说明 |
|------|------|------|
| date | date | 生产日期 |
| planned_quantity | int | 排产数量 |
| actual_output | int | 实际产出 |
| capacity_achievement_rate | float | 产能达成率 (%) |
| first_pass_rate | float | 一次直通率 (%) |
| material_utilization_rate | float | 材料利用率 (%) |
| daily_human_efficiency | float | 日人效 (元/人) |
| attendance_headcount | int | 出勤人头 |
| total_labor_cost | float | 总工费额 (元) |
| gross_profit | float | 毛利额 (元) |
| gross_profit_rate | float | 毛利率 (%) |
| material_ratio | float | 料占比 (%) |
| labor_ratio | float | 工占比 (%) |
| overhead_ratio | float | 费占比 (%) |

### 2.2 智能分析结果 (AnalysisResult)

```json
{
  "summary": "成本动因总览",
  "key_findings": ["关键发现1", "关键发现2"],
  "labor_efficiency": {
    "findings": ["人工与效率问题"],
    "root_causes": ["根本原因"],
    "actions": ["可落地动作"]
  },
  "quality_cost": {
    "findings": ["质量成本问题"],
    "root_causes": ["根本原因"],
    "actions": ["可落地动作"]
  },
  "improvement_plan": {
    "priority_actions": [
      {"action": "动作描述", "expected_impact": "预期效果", "priority": "高/中/低"}
    ]
  }
}
```

## 3. 分析维度

### 3.1 成本动因总览
- 整体成本结构分析（料/工/费占比）
- 毛利率异常预警
- 成本占比波动原因

### 3.2 人工与效率动因
- 产能达成率与出勤人头的匹配度
- 日人效异常分析
- 总工费额与产出比率

### 3.3 质量成本动因
- 一次直通率对毛利的影响
- 材料利用率与质量关系
- 返工/报废成本估算

### 3.4 改善方案
- 针对每个问题输出可落地动作
- 标明预期效果和优先级

## 4. API 设计

### POST /api/analysis/daily-cost

**Request Body:**
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

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "summary": "...",
    "key_findings": [...],
    "labor_efficiency": {...},
    "quality_cost": {...},
    "improvement_plan": {...}
  }
}
```

## 5. Prompt 设计原则

1. **角色设定**: 扮演制造业成本分析专家
2. **分析逻辑**: 数据对比 → 异常识别 → 根因推断 → 动作建议
3. **输出约束**: 简洁、可操作、突出重点
4. **安全边界**: 不编造数据，只基于提供的数据进行分析
