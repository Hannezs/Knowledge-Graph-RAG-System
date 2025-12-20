from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.db_utils import test_opengauss_connection
from utils.milvus_utils import test_milvus_operation
from routers import resource, ai, user, graph

app = FastAPI(title="知识图谱系统API")

# 配置跨域（允许Vue项目访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue默认运行地址，必须准确
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法（GET/POST等）
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由
app.include_router(resource.router)
app.include_router(ai.router)
app.include_router(user.router)
app.include_router(graph.router)

# 测试接口：/api/health
@app.get("/api/health")
async def health_check():
    # 同时验证数据库连接状态
    opengauss_ok = test_opengauss_connection()
    milvus_ok = test_milvus_operation()
    
    return {
        "status": "healthy" if (opengauss_ok and milvus_ok) else "unhealthy",
        "message": "FastAPI 服务正常运行",
        "databases": {
            "openGauss": "connected" if opengauss_ok else "disconnected",
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