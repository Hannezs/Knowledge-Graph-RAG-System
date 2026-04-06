from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from utils.milvus_utils import insert_vector
from utils.multimodal_utils import generate_text_embedding
from utils.db_utils import create_resource, list_resources
import uuid

router = APIRouter(prefix="/api/resource", tags=["Resource"])

@router.post("/upload")
async def upload_resource(file: UploadFile = File(...), user_id: str = "test_user"): # TODO: Get user_id from token
    # 1. 处理文件（示例：PDF提取文本并生成向量）
    content = await file.read()
    # TODO: Implement actual text extraction from PDF/Image
    # For now, assume content is text or handle appropriately
    # vector = generate_text_embedding(content)  # CLIP生成1024维向量
    
    # Mock vector for now if generate_text_embedding fails or needs text
    vector = [0.1] * 1024 
    
    # 2. 生成res_id（UUID，与openGauss中的res_id一致）
    res_id = str(uuid.uuid4()).replace('-', '')[:32]
    
    # 3. 存入 OpenGauss
    try:
        create_resource(res_id, file.filename, "PDF", user_id) # Assuming PDF for now
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 4. 调用milvus_utils插入向量
    try:
        insert_vector(res_id=res_id, vector=vector, vector_type="PDF")
    except Exception as e:
        # Rollback DB? For now just report error
        raise HTTPException(status_code=500, detail=f"Milvus error: {str(e)}")
    
    return {"code": 200, "msg": "上传成功", "res_id": res_id}

@router.get("/list")
async def list_all_resources(limit: int = 10, offset: int = 0):
    try:
        resources = list_resources(limit, offset)
        return {"code": 200, "data": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
