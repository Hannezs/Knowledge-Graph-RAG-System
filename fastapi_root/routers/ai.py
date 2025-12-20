import shutil
import os
import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from services.extraction_service import extract_knowledge
from services.rag_service import rag_qa
from utils.multimodal_utils import extract_text_from_pdf, parse_table_to_json

router = APIRouter(prefix="/api/ai", tags=["AI智能服务"])

class ExtractRequest(BaseModel):
    text: str

import uuid
from typing import Optional

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

@router.post("/extract/file")
async def extract_knowledge_from_file(file: UploadFile = File(...)):
    """
    上传文件进行知识抽取 (支持 PDF, CSV, Excel, TXT)
    """
    # 1. 保存临时文件
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. 根据文件类型解析内容
        text_content = ""
        filename = file.filename.lower()
        
        if filename.endswith(".pdf"):
            text_content = extract_text_from_pdf(file_path)
        elif filename.endswith((".csv", ".xls", ".xlsx")):
            # 表格转为 JSON 字符串作为文本处理
            data = parse_table_to_json(file_path)
            text_content = json.dumps(data, ensure_ascii=False, indent=2)
        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()
        else:
            raise HTTPException(status_code=400, detail="不支持的文件格式。仅支持 PDF, Excel, CSV, TXT")
            
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="文件内容解析为空")

        # 3. 调用抽取服务
        result = extract_knowledge(text_content)
        
        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result.get("reason", "抽取失败"))
            
        return result
        
    except Exception as e:
        print(f"❌ 文件处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")
    finally:
        # 清理临时文件
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@router.post("/extract")
async def extract_knowledge_endpoint(request: ExtractRequest):
    """
    提交文本进行知识抽取（实体与关系），并自动存入图数据库
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="文本内容不能为空")
    
    # 调用 extraction_service 进行处理
    result = extract_knowledge(request.text)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=500, detail=result.get("reason", "抽取失败"))
        
    return result

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    RAG 问答接口：基于知识库回答用户问题 (支持多轮对话)
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    # 如果没有 session_id，生成一个新的
    session_id = request.session_id or str(uuid.uuid4())
        
    # 调用 rag_service 进行问答
    answer = rag_qa(request.query, session_id=session_id)
    
    return {
        "answer": answer,
        "session_id": session_id
    }
