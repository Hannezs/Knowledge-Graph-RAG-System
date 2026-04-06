import psycopg2
from psycopg2 import OperationalError, pool
from contextlib import contextmanager
import uuid
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 数据库连接信息 (使用 .env 配置，现在是 Docker 版 PostgreSQL)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "dbname": os.getenv("DB_NAME", "knowledge_graph"),
    "sslmode": "disable" # 本地 Docker 环境不支持/要求强制 SSL
}

# 创建连接池
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **DB_CONFIG
    )
    print("✅ PostgreSQL 连接池初始化成功 (本地Docker环境)")
except Exception as e:
    print(f"❌ PostgreSQL 连接池初始化失败: {e}")
    db_pool = None

@contextmanager
def get_db_cursor():
    """获取数据库连接和游标的上下文管理器"""
    conn = None
    try:
        if db_pool:
            conn = db_pool.getconn()
            yield conn.cursor()
            conn.commit()
        else:
            raise Exception("数据库连接池未初始化")
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn and db_pool:
            db_pool.putconn(conn)

def test_postgres_connection():
    """测试PostgreSQL连接是否成功"""
    try:
        with get_db_cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()
            print(f"✅ PostgreSQL 连接成功，版本：{result[0]}")
            return True
    except Exception as e:
        print(f"❌ PostgreSQL 连接失败：{str(e)}")
        return False

# --- CRUD 操作封装 ---

# 1. 用户 (User)
# 表名: sys_user
# 字段: user_id, username, password, email, create_time
def get_user_by_username(username):
    sql = "SELECT user_id, username, password, email FROM sys_user WHERE username = %s;"
    try:
        with get_db_cursor() as cur:
            cur.execute(sql, (username,))
            result = cur.fetchone()
            if result:
                return {
                    "user_id": result[0],
                    "username": result[1],
                    "password": result[2],
                    "email": result[3]
                }
            return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def create_user(username, password, email=None):
    user_id = str(uuid.uuid4()).replace('-', '')[:32]
    sql = "INSERT INTO sys_user (user_id, username, password, email) VALUES (%s, %s, %s, %s) RETURNING user_id;"
    with get_db_cursor() as cur:
        cur.execute(sql, (user_id, username, password, email))
        return cur.fetchone()[0]

# 2. 资料 (Resource)
# 表名: resource, 字段: res_id, user_id, res_name, res_type, tags, upload_time
def create_resource(res_id, res_name, res_type, user_id, tags=None):
    sql = """
    INSERT INTO resource (res_id, user_id, res_name, res_type, tags, upload_time) 
    VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING res_id;
    """
    with get_db_cursor() as cur:
        cur.execute(sql, (res_id, user_id, res_name, res_type, tags))
        return cur.fetchone()[0]

def get_resource(res_id):
    sql = "SELECT * FROM resource WHERE res_id = %s;"
    with get_db_cursor() as cur:
        cur.execute(sql, (res_id,))
        return cur.fetchone()

def list_resources(limit=10, offset=0):
    # 修正字段名以匹配 create_resource
    sql = "SELECT res_id, res_name, upload_time, res_type FROM resource ORDER BY upload_time DESC LIMIT %s OFFSET %s;"
    with get_db_cursor() as cur:
        cur.execute(sql, (limit, offset))
        rows = cur.fetchall()
        return [
            {
                "resource_id": row[0],
                "filename": row[1],
                "upload_time": row[2],
                "type": row[3]
            }
            for row in rows
        ]

# 3. 实体 (Entity)
# 表名: entity, 字段: entity_id, entity_name, entity_type
def create_entity(entity_name, entity_type):
    # 1. 先查询是否存在
    check_sql = "SELECT entity_id FROM entity WHERE entity_name = %s AND entity_type = %s;"
    with get_db_cursor() as cur:
        cur.execute(check_sql, (entity_name, entity_type))
        result = cur.fetchone()
        if result:
            return result[0]  # 如果存在，直接返回旧ID

    # 2. 如果不存在，则插入
    entity_id = str(uuid.uuid4()).replace('-', '')[:32]
    sql = "INSERT INTO entity (entity_id, entity_name, entity_type) VALUES (%s, %s, %s) RETURNING entity_id;"
    try:
        with get_db_cursor() as cur:
            cur.execute(sql, (entity_id, entity_name, entity_type))
            return cur.fetchone()[0]
    except Exception:
        # 并发情况下可能仍会冲突，再次查询兜底
        with get_db_cursor() as cur:
            cur.execute(check_sql, (entity_name, entity_type))
            result = cur.fetchone()
            return result[0] if result else None

def batch_create_entities(entities_data):
    """
    批量创建实体
    :param entities_data: List[dict] -> [{"name": "n1", "type": "t1"}, ...]
    :return: Dict[(name, type), id]
    """
    if not entities_data:
        return {}

    # 去重
    unique_entities = {(e["name"], e["type"]) for e in entities_data}
    entity_map = {} # (name, type) -> id

    # 1. 查询已存在的实体
    try:
        with get_db_cursor() as cur:
            # 构建 WHERE 子句: (entity_name = 'n1' AND entity_type = 't1') OR ...
            # 注意：参数化查询处理大量数据时可能受限，这里假设数据量在合理范围内（<1000）
            # 更优解是使用临时表或 VALUES 列表 JOIN，为简化直接循环查询或分批查询
            # 这里采用分批查询优化
            
            # 简单起见，先查所有匹配的（如果数据量不大）
            # 或者构建一个大的 IN 查询 (name, type) IN (('n1', 't1'), ...)
            # Postgres 支持 tuple IN 语法
            
            conditions = []
            params = []
            for name, type_ in unique_entities:
                conditions.append("(%s, %s)")
                params.extend([name, type_])
            
            if not conditions:
                return {}
                
            where_clause = ",".join(conditions)
            sql = f"SELECT entity_name, entity_type, entity_id FROM entity WHERE (entity_name, entity_type) IN ({where_clause});"
            
            cur.execute(sql, tuple(params))
            for row in cur.fetchall():
                entity_map[(row[0], row[1])] = row[2]
    except Exception as e:
        print(f"Batch query failed: {e}")
        # Fallback to single queries if tuple syntax fails or other issue
        pass

    # 2. 找出需要插入的新实体
    new_entities = []
    for name, type_ in unique_entities:
        if (name, type_) not in entity_map:
            new_id = str(uuid.uuid4()).replace('-', '')[:32]
            new_entities.append((new_id, name, type_))
            entity_map[(name, type_)] = new_id
    
    if not new_entities:
        return entity_map

    # 3. 批量插入
    insert_sql = "INSERT INTO entity (entity_id, entity_name, entity_type) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
    try:
        with get_db_cursor() as cur:
            # executemany 实际上是多次执行，但比手动循环快
            # 使用 psycopg2.extras.execute_values 会更快，但这里先用标准库
            cur.executemany(insert_sql, new_entities)
    except Exception as e:
        print(f"Batch insert failed: {e}")
            
    return entity_map

# 4. 关系 (Relation)
# 表名: relation, 字段: rel_id, entity1_id, entity2_id, rel_type
def create_relation(entity1_id, entity2_id, rel_type):
    # 生成 32 位 UUID 作为 rel_id
    rel_id = str(uuid.uuid4()).replace('-', '')[:32]
    sql = "INSERT INTO relation (rel_id, entity1_id, entity2_id, rel_type) VALUES (%s, %s, %s, %s) RETURNING rel_id;"
    with get_db_cursor() as cur:
        cur.execute(sql, (rel_id, entity1_id, entity2_id, rel_type))
        return cur.fetchone()[0]

def batch_create_relations(relations_data):
    """
    批量创建关系
    :param relations_data: List[tuple] -> [(src_id, tgt_id, type), ...]
    """
    if not relations_data:
        return

    # 生成 ID 并准备数据
    insert_data = []
    for src, tgt, type_ in relations_data:
        rel_id = str(uuid.uuid4()).replace('-', '')[:32]
        insert_data.append((rel_id, src, tgt, type_))

    sql = "INSERT INTO relation (rel_id, entity1_id, entity2_id, rel_type) VALUES (%s, %s, %s, %s);"
    
    try:
        with get_db_cursor() as cur:
            cur.executemany(sql, insert_data)
    except Exception as e:
        print(f"Batch relation insert failed: {e}")

# 5. 图谱数据 (Graph) 查询
def get_graph_data(limit=100):
    # 获取节点
    entity_sql = "SELECT entity_id, entity_name, entity_type FROM entity LIMIT %s;"
    # 获取关系
    rel_sql = "SELECT rel_id, entity1_id, entity2_id, rel_type FROM relation LIMIT %s;"
    
    with get_db_cursor() as cur:
        cur.execute(entity_sql, (limit,))
        entities = [
            {"id": row[0], "name": row[1], "type": row[2]}
            for row in cur.fetchall()
        ]
        
        cur.execute(rel_sql, (limit,))
        relations = [
            {"id": row[0], "source": row[1], "target": row[2], "type": row[3]}
            for row in cur.fetchall()
        ]
        
    return {"nodes": entities, "links": relations}

# 6. 用户管理 (User Management)
def init_user_table():
    """初始化用户表"""
    sql = """
    CREATE TABLE IF NOT EXISTS sys_user (
        user_id VARCHAR(32) PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_db_cursor() as cur:
        try:
            cur.execute(sql)
            print("✅ 用户表(sys_user)初始化成功")
        except Exception as e:
            print(f"❌ 用户表(sys_user)初始化失败: {e}")

# 直接运行该文件测试
if __name__ == "__main__":
    test_postgres_connection()
    init_user_table()
