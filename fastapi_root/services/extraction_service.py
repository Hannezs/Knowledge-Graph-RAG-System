import json
import uuid
import concurrent.futures
from services.llm_service import call_llm
from utils.db_utils import create_entity, create_relation, batch_create_entities, batch_create_relations
from utils.milvus_utils import insert_vector
from utils.multimodal_utils import generate_text_embedding

def process_embedding(text_chunk: str):
    """后台任务：生成向量并存入Milvus"""
    try:
        # 生成唯一ID
        res_id = str(uuid.uuid4()).replace('-', '')[:32]
        # 生成向量
        vector = generate_text_embedding(text_chunk)
        # 存入Milvus (包含原始文本)
        insert_vector(res_id=res_id, vector=vector, vector_type="text", text=text_chunk)
        print(f"✅ 文本已向量化并存入Milvus, res_id: {res_id}")
        return res_id
    except Exception as e:
        print(f"⚠️ 向量化存储失败，但不影响图谱构建: {e}")
        return None

def extract_knowledge(text_chunk: str):
    """
    从文本中提取实体和关系，并构建知识图谱
    同时将文本向量化存入Milvus，用于RAG
    """
    system_prompt = """
    你是一个知识图谱构建专家。请从给定的文本中提取实体（Entity）和关系（Relation）。
    
    请严格按照以下 JSON 格式输出，不要包含任何其他解释性文字：
    {
        "entities": [
            {"name": "实体名1", "type": "实体类型1"},
            {"name": "实体名2", "type": "实体类型2"}
        ],
        "relations": [
            {"source": "实体名1", "target": "实体名2", "type": "关系类型"}
        ]
    }
    """
    
    response = ""
    
    # 1. 并行执行：向量化存储 + LLM抽取
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交向量化任务
        future_embedding = executor.submit(process_embedding, text_chunk)
        # 提交LLM任务
        future_llm = executor.submit(call_llm, prompt=text_chunk, system_prompt=system_prompt)
        
        # 等待LLM结果（这是主路径，必须等待）
        response = future_llm.result()
        
        # 向量化任务可以在后台继续，或者在这里等待确认
        # 为了确保数据一致性，这里选择等待，但因为是并行的，总耗时取决于最慢的那个
        future_embedding.result()

    # 2. 解析 JSON
    try:
        # 清洗可能存在的 Markdown 标记
        cleaned_response = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_response)
        
        entities = data.get("entities", [])
        relations = data.get("relations", [])
        
        print(f"🔍 提取到 {len(entities)} 个实体, {len(relations)} 条关系")
        
        # 3. 批量写入数据库 (OpenGauss)
        if entities:
            # 3.1 批量存实体 -> 返回 { (name, type): id }
            entity_map = batch_create_entities(entities)
            
            # 3.2 批量存关系
            relations_to_insert = []
            for rel in relations:
                src_name = rel["source"]
                tgt_name = rel["target"]
                
                # 查找对应的实体ID
                # 注意：这里需要处理实体类型匹配问题。
                # 简化起见，我们假设 LLM 返回的关系中的 source/target name 能在 entities 列表中找到
                # 并且我们尝试在 entity_map 中查找
                
                src_id = None
                tgt_id = None
                
                # 尝试匹配 source
                for (name, type_), id_ in entity_map.items():
                    if name == src_name:
                        src_id = id_
                        break
                
                # 尝试匹配 target
                for (name, type_), id_ in entity_map.items():
                    if name == tgt_name:
                        tgt_id = id_
                        break
                
                if src_id and tgt_id:
                    relations_to_insert.append((src_id, tgt_id, rel["type"]))
            
            if relations_to_insert:
                batch_create_relations(relations_to_insert)
                
        return {
            "status": "success", 
            "entities_count": len(entities), 
            "relations_count": len(relations),
            "data": {
                "entities": entities,
                "relations": relations
            }
        }
        
    except json.JSONDecodeError:
        print("❌ LLM返回格式错误，无法解析JSON")
        return {"status": "failed", "reason": "json_parse_error"}
    except Exception as e:
        print(f"❌ 知识图谱构建失败: {e}")
        return {"status": "failed", "reason": str(e)}
