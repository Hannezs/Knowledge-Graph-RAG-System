import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.db_utils import test_postgres_connection
from utils.milvus_utils import test_milvus_operation
try:
    from scripts.init_db import init_all_tables
except ImportError:
    init_all_tables = None
from routers import resource, ai, user, graph
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="知识图谱系统API")

# 从环境变量中读取允许的跨域白名单，默认提供 localhost 作为开发兜底
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 限制具体方法以提升安全性
    allow_headers=["*"],
)

# 启动时初始化数据库表
@app.on_event("startup")
async def startup_event():
    if init_all_tables:
        print("正在初始化数据库表结构...")
        init_all_tables()

# 注册路由
app.include_router(resource.router)
app.include_router(ai.router)
app.include_router(user.router)
app.include_router(graph.router)

# 测试接口：/api/health
@app.get("/api/health")
async def health_check():
    # 同时验证数据库连接状态
    postgres_ok = test_postgres_connection()
    milvus_ok = test_milvus_operation()
    
    return {
        "status": "healthy" if (postgres_ok and milvus_ok) else "unhealthy",
        "message": "FastAPI 服务正常运行",
        "databases": {
            "PostgreSQL": "connected" if postgres_ok else "disconnected",
            "Milvus": "connected" if milvus_ok else "disconnected"
        }
    }

# 新增：Milvus连接单独测试接口
@app.get("/api/test-milvus")
async def test_milvus_connection():
    """单独    单独测试Milvus向量数据库连接状态的专用接口
    """
    try:
        milvus_ok = test_milvus_operation()
        if milvus_ok:
            return {
                "status": "success",
                "message": "Milvus 连接成功",
                "details": "能够正常与Milvus向量数据库建立连接并执行操作"
            }
        else:
            return {
                "status": "failed",
                "message": "Milvus 连接失败",
                "details": "无法与Milvus向量数据库建立连接或执行操作"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "测试Milvus连接时发生异常",
            "error_details": str(e)
        }

 # FastAPI 推荐用命令行启动：
 # uvicorn main:app --reload