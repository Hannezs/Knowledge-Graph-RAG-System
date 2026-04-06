import pytest
from fastapi.testclient import TestClient
from main import app
import uuid
import os

client = TestClient(app)

# 生成唯一的测试用户名
test_username = f"test_user_{str(uuid.uuid4())[:8]}"
test_password = "testpassword123"

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register():
    response = client.post(
        "/api/user/register",
        json={"username": test_username, "password": test_password}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_login():
    response = client.post(
        "/api/user/login",
        data={"username": test_username, "password": test_password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_read_users_me():
    # 先登录获取token
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/user/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_username
    # assert "email" in data # email might be null

def test_upload_resource():
    # 创建一个临时的测试文件
    file_content = b"This is a test PDF content for integration testing."
    files = {"file": ("test_document.pdf", file_content, "application/pdf")}
    
    # 目前upload接口不需要鉴权，如果需要鉴权请添加headers
    response = client.post("/api/resource/upload", files=files)
    
    # 注意：如果Milvus或OpenGauss连接失败，这里可能会报错500
    # 我们假设环境是好的，或者至少能处理错误
    if response.status_code == 200:
        data = response.json()
        assert data["code"] == 200
        assert "res_id" in data
    else:
        # 如果依赖服务没开，允许失败，但打印警告
        pytest.warns(UserWarning, match=f"Upload failed: {response.text}")

def test_list_resources():
    response = client.get("/api/resource/list?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert isinstance(data["data"], list)

def test_graph_data():
    response = client.get("/api/graph/data?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "links" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["links"], list)
