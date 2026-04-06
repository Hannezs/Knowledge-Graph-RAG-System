import random
from typing import List, Any
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 设置 Hugging Face 镜像地址，解决国内连接问题
os.environ["HF_ENDPOINT"] = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")

# 尝试导入依赖库，如果未安装则提供提示
try:
    import PyPDF2
    import pandas as pd
    from PIL import Image
    from sentence_transformers import SentenceTransformer
    
    # 使用 ModelScope 下载稳定、抗网络干扰的中文 Embedding 模型
    # (iic/nlp_corom_sentence-embedding_chinese-base 同样输出 768 维的高质量中文向量)
    print("⏳ 正在加载 Embedding 模型 (基于阿里 ModelScope 源)...")
    from modelscope import snapshot_download
    
    # 强制从 ModelScope 国内源下载（已在你的环境中安装 modelscope）
    model_dir = snapshot_download('iic/nlp_corom_sentence-embedding_chinese-base')
    
    # 填入本地缓存路径加载
    embedding_model = SentenceTransformer(model_dir)
    print("✅ Embedding 模型加载完成")
    
except ImportError as e:
    print(f"⚠️ 缺少多模态处理依赖库: {e.name}。请运行 pip install -r requirements.txt 安装。")
    embedding_model = None

def extract_text_from_pdf(file_path: str) -> str:
    """
    从PDF文件中提取文本
    """
    text_content = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
    except Exception as e:
        print(f"❌ PDF解析失败: {e}")
    return text_content

def parse_table_to_json(file_path: str) -> List[dict]:
    """
    将Excel/CSV表格转换为JSON结构
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            return []
        
        # 转换为字典列表
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"❌ 表格解析失败: {e}")
        return []

def generate_text_embedding(content: Any) -> List[float]:
    """
    生成文本嵌入向量 (768维)
    """
    if embedding_model:
        try:
            # 确保输入是字符串
            text = str(content)
            # 生成向量
            embedding = embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"❌ 向量生成失败: {e}")
            return [0.0] * 768
    else:
        print("⚠️ Embedding模型未加载，返回随机向量")
        return [random.random() for _ in range(768)]

def generate_image_embedding(image_path: str) -> List[float]:
    """
    模拟生成图片嵌入向量。
    """
    # TODO: 集成实际的 CLIP 模型
    # image = Image.open(image_path)
    # inputs = processor(images=image, return_tensors="pt", padding=True)
    # outputs = model.get_image_features(**inputs)
    
    # 临时返回随机向量 (768维)
    return [random.random() for _ in range(768)]

