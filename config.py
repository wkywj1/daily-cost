import os
from dotenv import load_dotenv

load_dotenv()

# LLM 配置
LLMProvider = os.getenv("LLM_PROVIDER", "openai")  # openai / deepseek / zhipu
LLMModel = os.getenv("LLM_MODEL", "gpt-4o")
LLMApiKey = os.getenv("LLM_API_KEY", "")
LLMBaseUrl = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

# 业务配置
DefaultCurrency = "元"
AnalysisLanguage = "zh-CN"
