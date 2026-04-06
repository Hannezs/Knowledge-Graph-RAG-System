import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 配置你的模型信息
# 建议将 API_KEY 放入环境变量或 .env 文件中
API_KEY = os.getenv("LLM_API_KEY")
if not API_KEY:
    raise ValueError("严重安全警告: 未找到 LLM_API_KEY 环境变量！请在 .env 文件中配置以防止安全泄漏和功能失效。")

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

def call_llm_stream(prompt: str, system_prompt: str = "你是一个乐于助人的AI助手。"):
    """
    流式大模型调用接口
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"❌ LLM流式调用失败: {e}")
        yield "抱歉，AI 思考过程中遇到了问题。"
