from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from pymilvus.exceptions import MilvusException
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 本地Milvus连接配置（重点：host为localhost/127.0.0.1，端口19530，无token）
LOCAL_MILVUS_CONFIG = {
    "host": os.getenv("MILVUS_HOST", "127.0.0.1"),  # 本地地址，也可写"localhost"
    "port": os.getenv("MILVUS_PORT", "19530"),      # Milvus默认端口，不要改（除非你部署时自定义了）
    "alias": "default"    # 连接别名，固定即可
}

def connect_milvus():
    """建立本地Milvus连接，返回连接状态"""
    try:
        # 连接本地Milvus（无token，无需额外参数）
        connections.connect(**LOCAL_MILVUS_CONFIG)
        print("✅ 本地Milvus连接成功！")
        return True
    except MilvusException as e:
        print(f"❌ 本地Milvus连接失败：{e.message}")
        return False
    except Exception as e:
        print(f"❌ 未知错误：{str(e)}")
        return False

def disconnect_milvus():
    """关闭Milvus连接"""
    try:
        connections.disconnect(LOCAL_MILVUS_CONFIG["alias"])
        print("✅ Milvus连接已关闭")
    except:
        pass

def insert_vector(res_id: str, vector: list, vector_type: str, text: str = ""):
    """
    向Milvus插入向量
    :param res_id: 资源ID (32位字符串)
    :param vector: 向量数据 (list of floats)
    :param vector_type: 向量类型 (如 "PDF", "IMAGE")
    :param text: 原始文本内容 (用于RAG)
    """
    collection_name = "resource_vector_v3"  # 升级集合名称以适应新维度(768)
    
    # 1. 确保连接
    connect_milvus()
    
    # 2. 检查并创建集合（如果不存在）
    if not utility.has_collection(collection_name):
        fields = [
            FieldSchema(name="pk_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="res_id", dtype=DataType.VARCHAR, max_length=32),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768), # 维度改为768
            FieldSchema(name="vector_type", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=60000) # 增加文本字段
        ]
        schema = CollectionSchema(fields=fields, description="资源向量集合V3")
        coll = Collection(name=collection_name, schema=schema)
        # 创建索引 (CLIP模型推荐使用COSINE相似度)
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        coll.create_index(field_name="vector", index_params=index_params)
        print(f"✅ 已创建集合 {collection_name}")
    
    # 3. 插入数据
    collection = Collection(collection_name)
    # 数据格式必须按字段顺序或者是字典列表，这里按列插入
    # fields: [pk_id, res_id, vector, vector_type, text]
    data = [
        [res_id],       # res_id列
        [vector],       # vector列
        [vector_type],  # vector_type列
        [text]          # text列
    ]
    
    res = collection.insert(data)
    collection.flush()
    print(f"✅ 成功插入向量，res_id: {res_id}, Milvus ID: {res.primary_keys}")
    return res

def search_similar_vectors(query_vector: list, top_k: int = 5):
    """
    根据查询向量搜索相似资源
    :param query_vector: 查询向量 (768维)
    :param top_k: 返回结果数量
    :return: 搜索结果列表
    """
    collection_name = "resource_vector_v3" # 使用新集合
    connect_milvus()
    
    if not utility.has_collection(collection_name):
        print(f"❌ 集合 {collection_name} 不存在")
        return []
        
    collection = Collection(collection_name)
    collection.load()
    
    search_params = {
        "metric_type": "COSINE", 
        "params": {"nprobe": 10}
    }
    
    results = collection.search(
        data=[query_vector], 
        anns_field="vector", 
        param=search_params, 
        limit=top_k,
        output_fields=["res_id", "vector_type", "text"] # 获取text字段
    )
    
    # 解析结果
    hits = []
    for hit in results[0]:
        hits.append({
            "res_id": hit.entity.get("res_id"),
            "score": hit.distance,
            "type": hit.entity.get("vector_type"),
            "text": hit.entity.get("text") # 返回文本
        })
        
    return hits

def test_milvus_operation():
    """测试连接后的基础操作（创建集合、插入向量、建索引、查询）"""
    if not connect_milvus():
        return False
    
    collection_name = "local_test_collection"
    try:
        # 1. 删除旧集合+创建新集合
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024)
        ]
        schema = CollectionSchema(fields=fields, description="本地Milvus测试集合")
        coll = Collection(name=collection_name, schema=schema)
        print(f"✅ 成功创建测试集合：{collection_name}")

        # 2. 插入测试向量+刷盘
        test_vectors = [[0.1]*1024]
        insert_result = coll.insert([test_vectors])
        coll.flush()
        print(f"✅ 成功插入测试向量，ID：{insert_result.primary_keys}")

        # 3. 关键步骤：为vector字段创建索引（必须！否则搜索失败）
        index_params = {
            "index_type": "IVF_FLAT",  # 入门常用索引，简单易操作
            "metric_type": "L2",       # 距离计算方式（欧氏距离）
            "params": {"nlist": 128}   # 索引参数（nlist是聚类数量）
        }
        coll.create_index(field_name="vector", index_params=index_params)
        print(f"✅ 成功为vector字段创建IVF_FLAT索引")

        # 4. 加载集合+搜索
        coll.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = coll.search(
            data=[[0.1]*1024],
            anns_field="vector",
            param=search_params,
            limit=1
        )
        print(f"✅ 搜索结果：距离={results[0][0].distance}（0表示完全匹配）")
        return True
    except MilvusException as e:
        print(f"❌ Milvus操作失败：{e.message}")
        return False
    finally:
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
        disconnect_milvus()

# 直接运行测试
if __name__ == "__main__":
    test_milvus_operation()