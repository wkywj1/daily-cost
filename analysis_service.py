import json
from typing import Dict, Any
from models import ProductionDailyData, AnalysisResult
import config


# 系统 Prompt - 设定分析专家角色
SYSTEM_PROMPT = """你是一位制造业日成本分析专家。你的职责是基于生产日报数据，分析成本动因并给出可落地的改善建议。

分析维度：
1. 成本动因总览：整体成本结构（料/工/费占比）、毛利率异常预警
2. 人工与效率动因：产能达成率、出勤人头、日人效、总工费额分析
3. 质量成本动因：一次直通率、材料利用率对成本的影响
4. 改善方案：针对发现的问题，给出具体可落地的改善动作

输出要求：
- 基于提供的数据进行分析，不编造任何数据
- 发现问题要明确指出异常程度
- 改善动作要具体可执行
- 语言简洁专业，突出重点
- 全部使用中文输出

请严格按以下 JSON 格式输出，不要包含任何其他内容：
{
  "summary": "成本动因总览描述，2-3句话概括今日整体情况",
  "key_findings": ["关键发现1", "关键发现2", "关键发现3"],
  "labor_efficiency": {
    "findings": ["人工效率问题1", "人工效率问题2"],
    "root_causes": ["原因1", "原因2"],
    "actions": ["动作1", "动作2"]
  },
  "quality_cost": {
    "findings": ["质量问题1", "质量问题2"],
    "root_causes": ["原因1", "原因2"],
    "actions": ["动作1", "动作2"]
  },
  "improvement_plan": {
    "priority_actions": [
      {"action": "具体动作描述", "expected_impact": "预期效果", "priority": "高"},
      {"action": "具体动作描述", "expected_impact": "预期效果", "priority": "中"}
    ]
  }
}"""


def build_user_prompt(data: ProductionDailyData) -> str:
    """构建用户分析 prompt"""
    return f"""请分析以下 {data.date} 的生产日报数据：

【生产数据】
- 排产数量: {data.planned_quantity}
- 实际产出: {data.actual_output}
- 产能达成率: {data.capacity_achievement_rate}%
- 一次直通率: {data.first_pass_rate}%
- 材料利用率: {data.material_utilization_rate}%
- 日人效: {data.daily_human_efficiency} 元/人
- 出勤人头: {data.attendance_headcount}
- 总工费额: {data.total_labor_cost} 元
- 毛利额: {data.gross_profit} 元
- 毛利率: {data.gross_profit_rate}%
- 料占比: {data.material_ratio}%
- 工占比: {data.labor_ratio}%
- 费占比: {data.overhead_ratio}%

请进行智能分析并输出 JSON 结果。"""


def parse_llm_response(response_text: str) -> Dict[str, Any]:
    """解析 LLM 返回的 JSON"""
    # 尝试提取 JSON 块
    text = response_text.strip()
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        text = text[start:end].strip()

    return json.loads(text)


def call_llm(prompt: str) -> str:
    """调用 LLM API"""
    # 根据配置选择不同的 LLM provider
    if config.LLMProvider == "openai":
        return call_openai(prompt)
    elif config.LLMProvider == "deepseek":
        return call_deepseek(prompt)
    elif config.LLMProvider == "zhipu":
        return call_zhipu(prompt)
    else:
        raise ValueError(f"不支持的 LLM Provider: {config.LLMProvider}")


def call_openai(prompt: str) -> str:
    """调用 OpenAI API"""
    from openai import OpenAI
    client = OpenAI(
        api_key=config.LLMApiKey,
        base_url=config.LLMBaseUrl
    )
    response = client.chat.completions.create(
        model=config.LLMModel,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2048
    )
    return response.choices[0].message.content


def call_deepseek(prompt: str) -> str:
    """调用 DeepSeek API"""
    import requests
    url = f"{config.LLMBaseUrl}/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config.LLMApiKey}"}
    payload = {
        "model": config.LLMModel,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def call_zhipu(prompt: str) -> str:
    """调用智谱 AI API"""
    import requests
    url = f"{config.LLMBaseUrl}/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config.LLMApiKey}"}
    payload = {
        "model": config.LLMModel,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


async def analyze_production_data(data: ProductionDailyData) -> AnalysisResult:
    """
    智能分析生产日报数据

    Args:
        data: 生产日报数据

    Returns:
        AnalysisResult: 分析结果
    """
    user_prompt = build_user_prompt(data)
    response_text = call_llm(user_prompt)
    result_dict = parse_llm_response(response_text)

    return AnalysisResult(**result_dict)
