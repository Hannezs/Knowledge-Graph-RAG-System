<template>
  <div class="extraction-container">
    <div class="header">
      <h2>⛏️ 知识抽取与入库</h2>
      <p class="subtitle">支持文本输入或文件上传，AI将自动提取实体与关系并存入图数据库</p>
    </div>

    <div class="content">
      <el-row :gutter="20">
        <!-- 左侧：输入区 -->
        <el-col :span="10">
          <el-card class="box-card">
            <template #header>
              <div class="card-header">
                <span>📄 数据来源</span>
              </div>
            </template>

            <el-tabs v-model="activeTab" class="input-tabs">
              <el-tab-pane label="📝 文本输入" name="text">
                <el-input
                  v-model="inputText"
                  :rows="15"
                  type="textarea"
                  placeholder="请输入需要进行知识抽取的文本内容..."
                />
                <div class="actions">
                  <el-button type="primary" @click="handleExtract" :loading="loading" size="large">
                    🚀 开始抽取并入库
                  </el-button>
                </div>
              </el-tab-pane>

              <el-tab-pane label="📂 文件上传" name="file">
                <div class="upload-container">
                  <el-upload
                    class="upload-demo"
                    drag
                    action="#"
                    :http-request="handleFileUpload"
                    :show-file-list="false"
                    accept=".pdf,.txt,.csv,.xls,.xlsx"
                    :disabled="loading"
                  >
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                    <div class="el-upload__text">
                      拖拽文件到此处或 <em>点击上传</em>
                    </div>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持 PDF, Excel, CSV, TXT 文件
                      </div>
                    </template>
                  </el-upload>
                  <div v-if="loading" class="upload-loading">
                    <el-icon class="is-loading"><loading /></el-icon>
                    <span>正在解析文件并抽取知识...</span>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>

          </el-card>
        </el-col>

        <!-- 右侧：结果展示区 -->
        <el-col :span="14">
          <el-card class="box-card result-card">
            <template #header>
              <div class="card-header">
                <span>📊 抽取结果</span>
                <el-tag v-if="result" type="success">入库成功</el-tag>
              </div>
            </template>

            <div v-if="!result" class="empty-state">
              <el-empty description="暂无抽取结果，请在左侧输入文本并开始抽取" />
            </div>

            <div v-else class="result-content">
              <div class="stat-row">
                <el-statistic title="提取实体数" :value="result.entities_count" />
                <el-statistic title="提取关系数" :value="result.relations_count" />
              </div>

              <el-divider content-position="left">实体列表</el-divider>
              <el-table :data="result.data.entities" style="width: 100%" height="250">
                <el-table-column prop="name" label="实体名称" />
                <el-table-column prop="type" label="实体类型">
                  <template #default="scope">
                    <el-tag size="small">{{ scope.row.type }}</el-tag>
                  </template>
                </el-table-column>
              </el-table>

              <el-divider content-position="left">关系列表</el-divider>
              <el-table :data="result.data.relations" style="width: 100%" height="250">
                <el-table-column prop="source" label="源实体" />
                <el-table-column prop="type" label="关系类型">
                  <template #default="scope">
                    <el-tag type="warning" size="small">{{ scope.row.type }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="target" label="目标实体" />
              </el-table>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { UploadFilled, Loading } from '@element-plus/icons-vue';

const inputText = ref('');
const loading = ref(false);
const result = ref<any>(null);
const activeTab = ref('text');

const handleFileUpload = async (options: any) => {
  const file = options.file;
  if (!file) return;

  loading.value = true;
  result.value = null;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://localhost:8000/api/ai/extract/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    result.value = response.data;
    ElMessage.success('文件解析并抽取成功！');
  } catch (error: any) {
    console.error(error);
    ElMessage.error(error.response?.data?.detail || '文件处理失败');
  } finally {
    loading.value = false;
  }
};

const handleExtract = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本内容');
    return;
  }

  loading.value = true;
  result.value = null;

  try {
    const response = await axios.post('http://localhost:8000/api/ai/extract', {
      text: inputText.value
    });

    result.value = response.data;
    ElMessage.success('知识抽取并入库成功！');
  } catch (error: any) {
    console.error('抽取失败:', error);
    const msg = error.response?.data?.detail || '请求失败，请检查后端服务';
    ElMessage.error(msg);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.extraction-container {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.header {
  margin-bottom: 20px;
}

.subtitle {
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}

.content {
  flex: 1;
  overflow: hidden;
}

.box-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.result-content {
  overflow-y: auto;
  height: 100%;
}

.stat-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

:deep(.el-card__body) {
  flex: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.input-tabs {
  height: 100%;
  display: flex;
  flex-direction: column;
}
:deep(.el-tabs__content) {
  flex: 1;
  display: flex;
  flex-direction: column;
}
:deep(.el-tab-pane) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.upload-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.upload-loading {
  margin-top: 20px;
  color: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
</style>
