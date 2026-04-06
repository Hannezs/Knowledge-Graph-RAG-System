# 知识图谱与RAG问答系统 (Knowledge Graph & RAG System)

本项目是一个结合了**知识图谱 (Knowledge Graph)**和**检索增强生成 (RAG, Retrieval-Augmented Generation)**的智能问答与信息抽取系统。支持用户上传文档资源，自动抽取实体与关系构建知识图谱，并支持基于向量数据库的自然语言问答交互。

## 🛠️ 技术栈 (Tech Stack)

### 前端 (Frontend)
- **核心框架**: Vue 3 + TypeScript + Vite
- **UI 组件库**: Element Plus
- **路由**: Vue Router
- **图表展示**: ECharts / vue-d3-network (用于知识图谱的可视化呈现)
- **网络请求**: Axios

### 后端 (Backend)
- **核心框架**: FastAPI (Python)
- **数据库**: 
  - 关系型数据库: OpenGauss / PostgreSQL (存储用户、资源元数据、实体及关系)
  - 向量数据库: Milvus (存储文档切片及向量数据，支持语义检索)
- **核心库**: 
  - `sentence-transformers`: 文本向量化
  - `PyMilvus`: Milvus 向量数据库交互
  - `psycopg2`: OpenGauss/PostgreSQL 数据库交互
  - `PyPDF2`, `pandas`: 资源文件解析处理
  - `openai`: LLM 大语言模型服务集成

## 📂 项目结构 (Project Structure)

```text
.
├── ER_Diagram.md                # 数据库 E-R 图及概念模型
├── backend/                # Python FastAPI 后端服务目录
│   ├── main.py                  # API 服务入口文件
│   ├── requirements.txt         # 后端 Python 依赖列表
│   ├── routers/                 # API 路由层 (ai, graph, resource, user)
│   ├── services/                # 业务逻辑服务层 (基于LLM抽取、RAG模块)
│   ├── scripts/                 # 脚本目录 (如初始化 Milvus)
│   ├── utils/                   # 工具类 (数据库连接、Milvus 操作、通用多模态工具)
│   ├── tests/                   # 后端测试用例
│   └── temp_uploads/            # 临时资源上传目录
├── frontend/                # Vue3 前端应用目录
│   ├── src/
│   │   ├── views/               # 页面视图 (聊天、信息抽取、图谱展示、主页、登录注册)
│   │   ├── router/              # 前端路由配置
│   │   └── main.ts              # 前端应用入口
│   ├── package.json             # 前端依赖配置
│   └── vite.config.ts           # Vite 构建配置
└── infrastructure/                # 向量数据库 Milvus 的 Docker Compose 部署配置
    ├── docker-compose.yml       # 包含 etcd, MinIO 和 Milvus
    └── volumes/                 # 本地持久化数据卷
```

## ✨ 主要功能模块 (Core Features)

1. **用户认证 (User Module)**
   - 登录与注册。

2. **资源管理 (Resource Management)**
   - 多种格式文档（PDF/Excel等）的上传、解析与管理。

3. **知识图谱 (Knowledge Graph)**
   - **自动化抽取**: 通过大模型对上传的上传文档进行自动化抽取，生成 `实体 (Entity)` 和 `关系 (Relation)`。
   - **可视化**: 提取出的知识结构将以可视化的图谱形式展现。

4. **AI 问答助手 (RAG Chatbot)**
   - 将长文档切片（VectorChunk）并转为向量存入 Milvus。
   - 聊天界面可根据用户的问题进行语义搜索并结合大语言模型返回精准答案。

## 🚀 环境依赖与运行指南 (Getting Started)

### 1. 启动向量数据库 (Milvus)
依赖环境: `Docker` 和 `Docker Compose`
```bash
cd infrastructure
docker-compose up -d
```
请确保 Milvus (通常在 19530 端口) 以及依赖的 etcd 和 MinIO 正常运行。

### 2. 启动前端服务 (Frontend)
依赖环境: `Node.js` (要求 v20.19.0+ 或 v22.12.0+)
```bash
cd frontend
# 安装依赖
npm install
# 启动开发服务器 (默认端口 http://localhost:5173 )
npm run dev
```

### 3. 启动后端服务 (Backend)
依赖环境: `Python 3.8+`
```bash
cd backend
# 安装依赖
pip install -r requirements.txt
# 启动 FastAPI 服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 数据库初始化及测试
后端的 `FastAPI` 已经配置了 `/api/health` 检查端点，可以通过浏览器访问 `http://127.0.0.1:8000/api/health` 确认 OpenGauss 和 Milvus 的连接状态。

## 📖 数据库设计 (Database Schema)

相关实体的结构请参阅根目录下的 [`ER_Diagram.md`](./ER_Diagram.md)。
主要包含以下核心实体：
- **User & Resource**: 用户与上传的文件资源。
- **Entity & Relation**: 用于构建知识图谱的节点（实体）和边（关系）。
- **VectorChunk**: 结合 `Milvus` 用于 RAG 的向量数据块。