from services.llm_service import call_llm
from utils.milvus_utils import search_similar_vectors
from utils.multimodal_utils import generate_text_embedding

# 简单的内存会话历史存储 (生产环境建议使用 Redis)
CHAT_HISTORY = {}

def rag_qa(query: str, session_id: str = None):
    """
    RAG 问答核心逻辑 (支持多轮对话)
    """
    # 1. 问题向量化
    query_vector = generate_text_embedding(query)
    
    # 2. 向量检索 (Milvus)
    # 返回 top_k=3 个相关片段
    hits = search_similar_vectors(query_vector, top_k=3)
    
    # 3. 构建上下文
    context_list = []
    if hits:
        for hit in hits:
            text_content = hit.get('text', '')
            if text_content:
                context_list.append(f"[资料ID: {hit['res_id']}]\n{text_content}")
    
    context_str = "\n\n".join(context_list) if context_list else "（未找到相关资料）"
    
    # 4. 处理会话历史
    history_str = ""
    if session_id:
        if session_id not in CHAT_HISTORY:
            CHAT_HISTORY[session_id] = []
        
        # 获取最近 3 轮对话作为上下文
        recent_history = CHAT_HISTORY[session_id][-6:] 
        for msg in recent_history:
            role = "用户" if msg["role"] == "user" else "助手"
            history_str += f"{role}: {msg['content']}\n"

    # 5. 构建 Prompt
    prompt = f"""
    你是一个基于知识库的智能助手。请结合【参考资料】和【对话历史】回答【用户问题】。
    如果资料中没有答案，请尝试根据上下文回答，或者直接说不知道。
    
    【参考资料】：
    {context_str}
    
    【对话历史】：
    {history_str}
    
    【用户问题】：
    {query}
    """
    
    # 6. 调用大模型生成回答
    answer = call_llm(prompt)
    
    # 7. 更新历史
    if session_id:
        CHAT_HISTORY[session_id].append({"role": "user", "content": query})
        CHAT_HISTORY[session_id].append({"role": "assistant", "content": answer})
        
    return answer

from services.llm_service import call_llm_stream

def rag_qa_stream(query: str, session_id: str = None):
    query_vector = generate_text_embedding(query)
    hits = search_similar_vectors(query_vector, top_k=3)
    
    context_list = []
    if hits:
        for hit in hits:
            text_content = hit.get('text', '')
            if text_content:
                context_list.append(f"[资料ID: {hit['res_id']}]\n{text_content}")
    
    context_str = "\n\n".join(context_list) if context_list else "（未找到相关资料）"
    
    history_str = ""
    if session_id:
        if session_id not in CHAT_HISTORY:
            CHAT_HISTORY[session_id] = []
        recent_history = CHAT_HISTORY[session_id][-6:] 
        for msg in recent_history:
            role = "用户" if msg["role"] == "user" else "助手"
            history_str += f"{role}: {msg['content']}\n"

    prompt = f"""
    你是一个基于知识库的智能助手。请结合【参考资料】和【对话历史】回答【用户问题】。
    如果资料中没有答案，请尝试根据上下文回答，或者直接说不知道。
    
    【参考资料】：
    {context_str}
    
    【对话历史】：
    {history_str}
    
    【用户问题】：
    {query}
    """
    
    full_answer = ""
    for chunk in call_llm_stream(prompt):
        if chunk:
            full_answer += chunk
            yield chunk
            
    if session_id:
        CHAT_HISTORY[session_id].append({"role": "user", "content": query})
        CHAT_HISTORY[session_id].append({"role": "assistant", "content": full_answer})
