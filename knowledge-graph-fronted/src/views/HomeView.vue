<template>
  <div class="home-container">
    <!-- 欢迎区域 -->
    <div class="hero-section">
      <h1 class="title">欢迎使用知识图谱智能系统</h1>
      <p class="subtitle">基于大模型与图数据库的新一代知识管理平台</p>
    </div>

    <!-- 功能卡片区 -->
    <div class="features-section">
      <el-row :gutter="30">
        <el-col :span="8" v-for="feature in features" :key="feature.path">
          <el-card class="feature-card" shadow="hover" @click="$router.push(feature.path)">
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 系统状态监控 -->
    <div class="status-section">
      <el-card class="status-card">
        <template #header>
          <div class="card-header">
            <span>🖥️ 系统运行状态</span>
            <el-button type="primary" link @click="fetchHealthStatus" :loading="checking">
              刷新状态
            </el-button>
          </div>
        </template>

        <div class="status-grid">
          <div class="status-item">
            <span class="label">后端服务</span>
            <el-tag :type="healthData?.status === 'healthy' ? 'success' : 'danger'">
              {{ healthData?.status === 'healthy' ? '运行中' : '异常' }}
            </el-tag>
          </div>
          <div class="status-item">
            <span class="label">OpenGauss</span>
            <el-tag :type="healthData?.databases.openGauss === 'connected' ? 'success' : 'info'">
              {{ healthData?.databases.openGauss === 'connected' ? '已连接' : '未连接' }}
            </el-tag>
          </div>
          <div class="status-item">
            <span class="label">Milvus</span>
            <el-tag :type="healthData?.databases.Milvus === 'connected' ? 'success' : 'info'">
              {{ healthData?.databases.Milvus === 'connected' ? '已连接' : '未连接' }}
            </el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const checking = ref(false);

const features = [
  {
    title: '知识图谱可视化',
    desc: '直观展示实体与关系，支持交互式探索与查询',
    icon: '🕸️',
    path: '/graph'
  },
  {
    title: '智能知识抽取',
    desc: '上传文档或输入文本，自动提取知识并入库',
    icon: '⛏️',
    path: '/extraction'
  },
  {
    title: 'RAG 智能问答',
    desc: '基于知识库的精准问答，支持多轮对话',
    icon: '🤖',
    path: '/chat'
  }
];

interface HealthData {
  status: 'healthy' | 'unhealthy';
  message: string;
  databases: {
    openGauss: 'connected' | 'disconnected';
    Milvus: 'connected' | 'disconnected';
  };
}
const healthData = ref<HealthData | null>(null);

const fetchHealthStatus = async () => {
  checking.value = true;
  try {
    const response = await axios.get('http://localhost:8000/api/health');
    healthData.value = response.data;
    ElMessage.success('系统状态检测正常');
  } catch (error) {
    console.error('接口调用失败：', error);
    ElMessage.error('无法连接到后端服务');
    healthData.value = {
      status: 'unhealthy',
      message: 'Connection failed',
      databases: { openGauss: 'disconnected', Milvus: 'disconnected' }
    };
  } finally {
    checking.value = false;
  }
};

onMounted(() => {
  fetchHealthStatus();
});
</script>

<style scoped>
.home-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
}

.title {
  font-size: 36px;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #909399;
}

.features-section {
  margin-bottom: 60px;
}

.feature-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-card h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.feature-card p {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.status-section {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  text-align: center;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.label {
  color: #606266;
  font-size: 14px;
}
</style>
