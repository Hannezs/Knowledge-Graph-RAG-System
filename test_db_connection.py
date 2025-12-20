# 导入依赖包
import psycopg2
from psycopg2 import OperationalError
from pymilvus import connections, MilvusException

# ====================== 替换以下参数（关键！）======================
# openGauss连接参数（华为云实例）
OPENGauss_CONFIG = {
    "host": "121.36.73.114",  # 如：124.xxx.xxx.xxx
    "port": "26000",                  # 默认5432，若修改过则填实际值
    "user": "zyh",                  # 实例创建时的管理员账号（默认root）
    "password": "Lionel10", # 实例创建时设置的密码（如Test123!）
    "dbname": "knowledge_db" ,       # 已创建的目标数据库
    "sslmode": "require"  # 必须加这一行，适配openGauss的SSL要求
}

# Milvus连接参数（二选一：托管版/本地版）
# 1. 华为云托管版Milvus（填以下参数）
MILVUS_CONFIG = {
    "host": "1.92.67.57",    # 如：124.xxx.xxx.xxx
    "port": "19530",                 # 默认19530
    "user": "root",      # 托管版创建集群时设置的账号
    "password": "Hannes_zhang666"     # 托管版创建集群时设置的密码
}

# 2. 本地Docker部署Milvus（注释上面托管版，取消下面注释）
# MILVUS_CONFIG = {
#     "host": "localhost",           # 本地地址
#     "port": "19530",               # 默认19530，若改端口则填实际值
#     "user": "",                    # 本地版无需用户名
#     "password": ""                 # 本地版无需密码
# }
# ==================================================================

def test_opengauss_connection():
    """测试openGauss连接"""
    print("===== 开始测试openGauss连接 =====")
    try:
        # 建立连接
        conn = psycopg2.connect(
            host=OPENGauss_CONFIG["host"],
            port=OPENGauss_CONFIG["port"],
            user=OPENGauss_CONFIG["user"],
            password=OPENGauss_CONFIG["password"],
            dbname=OPENGauss_CONFIG["dbname"],
            sslmode=OPENGauss_CONFIG["sslmode"]  # 新增这一行
        )
        # 创建游标，验证连接可用
        cursor = conn.cursor()
        cursor.execute("SELECT version();")  # 执行简单查询
        db_version = cursor.fetchone()[0]
        print(f"✅ openGauss连接成功！")
        print(f"   数据库版本：{db_version[:50]}...")  # 只显示前50字符，避免过长
        
        # 关闭连接
        cursor.close()
        conn.close()
    except OperationalError as e:
        print(f"❌ openGauss连接失败！错误信息：{e}")
    except Exception as e:
        print(f"❌ openGauss连接异常！错误信息：{e}")

def test_milvus_connection():
    """测试Milvus连接"""
    print("\n===== 开始测试Milvus连接 =====")
    try:
        # 建立连接（托管版需传用户名密码，本地版无需）
        if MILVUS_CONFIG["user"] and MILVUS_CONFIG["password"]:
            connections.connect(
                alias="default",
                host=MILVUS_CONFIG["host"],
                port=MILVUS_CONFIG["port"],
                user=MILVUS_CONFIG["user"],
                password=MILVUS_CONFIG["password"]
            )
        else:
            connections.connect(
                alias="default",
                host=MILVUS_CONFIG["host"],
                port=MILVUS_CONFIG["port"]
            )
        # 验证连接：获取Milvus版本
        from pymilvus import utility
        milvus_version = utility.get_server_version()
        print(f"✅ Milvus连接成功！")
        print(f"   Milvus版本：{milvus_version}")
        
        # 关闭连接
        connections.disconnect("default")
    except MilvusException as e:
        print(f"❌ Milvus连接失败！错误信息：{e}")
    except Exception as e:
        print(f"❌ Milvus连接异常！错误信息：{e}")

if __name__ == "__main__":
    # 依次测试openGauss和Milvus连接
    test_opengauss_connection()
    test_milvus_connection()
    print("\n===== 连接测试完成 =====")