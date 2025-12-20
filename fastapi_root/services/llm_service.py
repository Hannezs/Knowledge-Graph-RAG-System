import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 配置你的模型信息
# 建议将 API_KEY 放入环境变量或 .env 文件中
API_KEY = os.getenv("LLM_API_KEY", "09ee494ef9a2478ca3d852fae7799132.neIecXyaatQRajS4")
BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")  # 如果是智谱/本地模型，请修改此地址
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "GLM-4.5-Flash")  # 或 "glm-4", "llama3" 等

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def call_llm(prompt: str, system_prompt: str = "你是一个乐于助人的AI助手。") -> str:
    """
    通用大模型调用接口
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # 知识抽取需要较低的随机性
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ LLM调用失败: {e}")
        return ""
