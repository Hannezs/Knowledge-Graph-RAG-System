from pymilvus import MilvusClient

# 连接本地Milvus（默认地址：http://localhost:19530，默认token：root:Milvus）
client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

# 1. 验证连接：列出所有集合（初始为空，返回[]）
print("当前集合列表：", client.list_collections())

# 2. 测试创建集合、插入向量（验证核心功能）
# 创建集合（向量维度设为1024，和CLIP生成的嵌入维度匹配）
client.create_collection(
    collection_name="test_collection",
    dimension=1024,  # 向量维度，需和你的AI模型输出一致
    primary_field_name="id",
    primary_field_type="INT64",
    auto_id=True
)

# 插入测试向量
vectors = [[0.1]*1024 for _ in range(5)]  # 生成5个1024维的测试向量
client.insert(collection_name="test_collection", data=[{"vector": v} for v in vectors])

# 3. 测试查询
res = client.search(
    collection_name="test_collection",
    data=[[0.1]*1024],  # 检索向量
    limit=3,
    output_fields=["id"]
)
print("检索结果：", res)

# 4. 清理测试数据（可选）
client.drop_collection(collection_name="test_collection")
print("测试完成，Milvus部署成功！")