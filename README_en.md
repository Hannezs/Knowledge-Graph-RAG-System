# Knowledge Graph & RAG System

<p align="center">
  <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg?logo=vue.js" alt="Vue 3">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Milvus-Database-0D85D8.svg?logo=milvus" alt="Milvus">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791.svg?logo=postgresql" alt="PostgreSQL">
</p>

[中文版 / Chinese Version](./README.md)

This project is an intelligent Question-Answering and Information Extraction system integrating **Knowledge Graph (KG)** and **Retrieval-Augmented Generation (RAG)** technologies. It allows users to upload document resources, automatically extracts entities and relationships to build a knowledge graph, and supports natural language interactive QA powered by a vector database and Large Language Models (LLMs).

## 🛠️ Tech Stack

### Frontend
- **Core Framework**: Vue 3 + TypeScript + Vite
- **UI Library**: Element Plus
- **Routing**: Vue Router
- **Visualization**: ECharts / vue-d3-network (for rendering knowledge graph nodes and edges)
- **HTTP Client**: Axios

### Backend
- **Core Framework**: FastAPI (Python)
- **Databases**: 
  - Relational Database: OpenGauss / PostgreSQL (stores users, resource metadata, entities, and relations)
  - Vector Database: Milvus (stores document chunks and vector embeddings for semantic search)
- **Core Libraries**: 
  - `sentence-transformers`: Text embedding/vectorization
  - `PyMilvus`: Milvus vector database client
  - `psycopg2`: OpenGauss/PostgreSQL database client
  - `PyPDF2`, `pandas`: Resource file parsing
  - `openai`: LLM service integration

## 📂 Project Structure

```text
.
├── ER_Diagram.md                # ER Diagram and conceptual models
├── backend/                # Python FastAPI backend directory
│   ├── main.py                  # API service entry point
│   ├── requirements.txt         # Backend Python dependencies
│   ├── routers/                 # API routing layer (ai, graph, resource, user)
│   ├── services/                # Business logic (LLM extraction, RAG logic)
│   ├── scripts/                 # Utility scripts (e.g., Milvus initialization)
│   ├── utils/                   # Helpers (DB connections, multimodal processing)
│   ├── tests/                   # Backend test cases
│   └── temp_uploads/            # Temporary directory for uploaded files
├── frontend/                # Vue3 frontend directory
│   ├── src/
│   │   ├── views/               # UI Views (Chat, Extraction, Graph, Home, Auth)
│   │   ├── router/              # Frontend routing configuration
│   │   └── main.ts              # Frontend entry point
│   ├── package.json             # Frontend dependencies
│   └── vite.config.ts           # Vite build configuration
└── infrastructure/                # Docker Compose setup for local Milvus DB
    ├── docker-compose.yml       # Includes etcd, MinIO, and Milvus services
    └── volumes/                 # Local persistent data volumes
```

## ✨ Core Features

1. **User Authentication (User Module)**
   - Registration and Login support.

2. **Resource Management**
   - Uploading, parsing, and management of various document formats (PDF, Excel, etc.).

3. **Knowledge Graph**
   - **Automated Extraction**: Analyzes uploaded documents using LLMs to automatically extract `Entities` and `Relations`.
   - **Visualization**: Visually presents the extracted knowledge structure as interactive graph networks.

4. **AI QA Assistant (RAG Chatbot)**
   - Slices long documents into chunks (VectorChunk), converts them into embeddings, and stores them in Milvus.
   - The chat interface allows users to ask questions; the system uses semantic search combined with LLMs to return accurate answers based on the uploaded knowledge base.

## 🚀 Getting Started

### 1. Start Vector Database (Milvus)
Dependencies: `Docker` and `Docker Compose`
```bash
cd infrastructure
docker-compose up -d
```
Ensure Milvus (usually on port 19530), etcd, and MinIO are running properly.

### 2. Start Frontend Service
Dependencies: `Node.js` (v20.19.0+ or v22.12.0+ required)
```bash
cd frontend
# Install dependencies
npm install
# Start dev server (default port: http://localhost:5173)
npm run dev
```

### 3. Start Backend Service
Dependencies: `Python 3.8+`
```bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Database Setup & Health Check
The FastAPI backend is configured with a health check endpoint. You can verify the connection status of both OpenGauss and Milvus by opening the following link in your browser:  
`http://127.0.0.1:8000/api/health`

## 📖 Database Schema

For detailed entity structures, refer to [`ER_Diagram.md`](./ER_Diagram.md) in the root directory.
The primary entities include:
- **User & Resource**: Accounts and the files they upload.
- **Entity & Relation**: Nodes (entities) and edges (relations) that construct the knowledge graph.
- **VectorChunk**: Vector data snippets stored in Milvus, dedicated to RAG semantic search.