from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

def init_milvus_collection():
    # 1. 连接本地Milvus
    connections.connect(
        alias="default",
        host="127.0.0.1",
        port="19530"
    )
    print("Milvus连接成功")

    # 2. 定义集合Schema
    fields = [
        FieldSchema(name="pk_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="res_id", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
        FieldSchema(name="vector_type", dtype=DataType.VARCHAR, max_length=20)
    ]
    schema = CollectionSchema(fields, description="多模态资源向量集合")

    # 3. 创建/重建集合（若已存在则删除重建）
    collection_name = "resource_vector"
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    collection = Collection(name=collection_name, schema=schema)

    # 4. 创建索引并加载
    index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
    collection.create_index(field_name="vector", index_params=index_params)
    collection.load()

    print(f"Milvus集合 {collection_name} 创建并加载成功")

if __name__ == "__main__":
    init_milvus_collection()