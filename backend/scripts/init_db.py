from utils.db_utils import get_db_cursor

def init_all_tables():
    """初始化知识图谱所需的所有PostgreSQL表"""
    
    sys_user_sql = """
    CREATE TABLE IF NOT EXISTS sys_user (
        user_id VARCHAR(32) PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    resource_sql = """
    CREATE TABLE IF NOT EXISTS resource (
        res_id VARCHAR(32) PRIMARY KEY,
        user_id VARCHAR(32),
        res_name VARCHAR(255),
        res_type VARCHAR(50),
        tags TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    entity_sql = """
    CREATE TABLE IF NOT EXISTS entity (
        entity_id VARCHAR(32) PRIMARY KEY,
        entity_name VARCHAR(255) NOT NULL,
        entity_type VARCHAR(100) NOT NULL,
        UNIQUE (entity_name, entity_type)
    );
    """
    
    relation_sql = """
    CREATE TABLE IF NOT EXISTS relation (
        rel_id VARCHAR(32) PRIMARY KEY,
        entity1_id VARCHAR(32) NOT NULL,
        entity2_id VARCHAR(32) NOT NULL,
        rel_type VARCHAR(100) NOT NULL
    );
    """
    
    with get_db_cursor() as cur:
        try:
            cur.execute(sys_user_sql)
            print("✅ 用户表(sys_user)检查/初始化成功")
        except Exception as e:
            print(f"❌ 用户表(sys_user)初始化失败: {e}")
            
        try:
            cur.execute(resource_sql)
            print("✅ 资源表(resource)检查/初始化成功")
        except Exception as e:
            print(f"❌ 资源表(resource)初始化失败: {e}")
            
        try:
            cur.execute(entity_sql)
            print("✅ 实体表(entity)检查/初始化成功")
        except Exception as e:
            print(f"❌ 实体表(entity)初始化失败: {e}")
            
        try:
            cur.execute(relation_sql)
            print("✅ 关系表(relation)检查/初始化成功")
        except Exception as e:
            print(f"❌ 关系表(relation)初始化失败: {e}")

if __name__ == "__main__":
    init_all_tables()
