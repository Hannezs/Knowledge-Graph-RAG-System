"""
测试本地数据库环境连接状态脚本
适用于当前 Docker Compose 部署的本地 PostgreSQL 和 Milvus
"""

import psycopg2
from pymilvus import connections, utility, MilvusException

# ====================== 本地环境连接配置 ======================
# PostgreSQL连接参数 (对应 milvus-local/docker-compose.yml 部署)
POSTGRES_CONFIG = {
    "host": "127.0.0.1",
    "port": "5432",
    "user": "postgres",
    "password": "postgres",
    "dbname": "knowledge_graph",
    "sslmode": "disable"  # 本地docker版PG一般不强制要求SSL
}

# Milvus连接参数 (对应本地 Standalone 版本)
MILVUS_CONFIG = {
    "alias": "default",
    "host": "127.0.0.1",
    "port": "19530"
}
# ==============================================================

def test_postgres_connection():
    """测试 PostgreSQL 连接"""
    print("===== 开始测试 PostgreSQL (本地 Docker环境) 连接 =====")
    try:
        # 建立连接
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        
        # 创建游标执行简单查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL 连接成功！")
        print(f"   服务器版本详情：{db_version}")
        
        # 检查当前连接数据库
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"   当前连接数据库名：{db_name}")
        
        # 释放资源
        cursor.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL 连接失败！请检查 Postgres 容器是否启动并在5432端口监听。\n   错误信息：{e}")
    except Exception as e:
        print(f"❌ PostgreSQL 连接出现异常！\n   错误信息：{e}")

def test_milvus_connection():
    """测试 Milvus 连接"""
    print("\n===== 开始测试 Milvus (本地 Standalone) 连接 =====")
    try:
        # 建立到本地Milvus的连接 (无需用户名密码)
        connections.connect(**MILVUS_CONFIG)
        
        # 获取Milvus服务器版本验证
        milvus_version = utility.get_server_version()
        print(f"✅ Milvus 连接成功！")
        print(f"   Milvus 引擎版本：{milvus_version}")
        
        # 获取当前集合列表，打印状态
        collections = utility.list_collections()
        print(f"   当前拥有的 Collections (集合): {collections}")
        
        connections.disconnect(MILVUS_CONFIG["alias"])
    except MilvusException as e:
        print(f"❌ Milvus 连接失败！请检查 Milvus 相关容器(包含etcd, minio)是否正常启动运行。\n   错误信息：{e}")
    except Exception as e:
        print(f"❌ Milvus 连接出现异常！\n   错误信息：{e}")

if __name__ == "__main__":
    print(f"开始本地环境状态诊断...\n")
    test_postgres_connection()
    test_milvus_connection()
    print("\n===== 环境诊断测试完成 =====")
