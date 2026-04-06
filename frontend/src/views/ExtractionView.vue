<template>
  <div class="h-[calc(100vh-100px)] flex flex-col bg-transparent p-0 md:p-2">
    <div class="mb-4 flex flex-col px-2">
      <h2 class="text-2xl font-normal text-[#202124] flex items-center gap-2 tracking-tight">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        {{ $t('extraction.title') }}
      </h2>
      <p class="text-sm text-[#5f6368] mt-1">{{ $t('extraction.desc') }}</p>
    </div>

    <div class="flex-1 flex flex-col md:flex-row gap-6 min-h-0">
      <!-- 左侧：输入区 -->
      <div class="w-full md:w-5/12 bg-white rounded-2xl shadow-sm border border-[#dadce0] flex flex-col overflow-hidden">
        <div class="px-6 py-4 border-b border-[#f1f3f4] font-medium text-lg text-[#3c4043] flex items-center gap-2 bg-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          {{ $t('extraction.dataSource') }}
        </div>
        
        <div class="flex-1 p-6 flex flex-col overflow-auto">
          <!-- 标签页导航 -->
          <div class="tabs tabs-boxed mb-4 bg-[#f1f3f4] p-1 rounded-xl">
            <a 
              class="tab flex-1 rounded-lg transition-all" 
              :class="activeTab === 'text' ? 'bg-white shadow-sm text-primary font-medium' : 'text-[#5f6368] hover:text-[#202124]'"
              @click="activeTab = 'text'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
              文本输入
            </a>
            <a 
              class="tab flex-1 rounded-lg transition-all" 
              :class="activeTab === 'file' ? 'bg-white shadow-sm text-primary font-medium' : 'text-[#5f6368] hover:text-[#202124]'"
              @click="activeTab = 'file'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" /></svg>
              文件上传
            </a>
          </div>

          <!-- 文本输入页 -->
          <div v-if="activeTab === 'text'" class="flex-1 flex flex-col">
            <textarea 
              v-model="inputText"
              class="textarea textarea-bordered flex-1 w-full resize-none font-mono focus:outline-none focus:border-primary"
              :placeholder="$t('extraction.textPlaceholder')"
              :disabled="loading"
            ></textarea>
            <div class="mt-4 flex justify-center">
              <button 
                @click="handleExtract" 
                :disabled="loading || !inputText.trim()"
                class="btn btn-primary w-full shadow-sm gap-2"
              >
                <span v-if="loading" class="loading loading-spinner"></span>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                开始抽取并入库
              </button>
            </div>
          </div>

          <!-- 文件上传页 -->
          <div v-else class="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-base-300 rounded-xl bg-base-200/50 p-8 text-center hover:border-primary transition-colors">
            <input 
              type="file" 
              id="file-upload" 
              class="hidden" 
              @change="onFileChange"
              accept=".pdf,.txt,.csv,.xls,.xlsx"
              :disabled="loading"
            />
            <label for="file-upload" class="cursor-pointer flex flex-col items-center gap-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-base-content/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
              <div>
                <p class="font-medium text-lg">{{ $t('extraction.clickToUpload') }}</p>
                <p class="text-sm opacity-50 mt-2">{{ $t('extraction.uploadHints') }}</p>
              </div>
              <button class="btn btn-outline btn-sm mt-2 pointer-events-none" :class="{ 'loading': loading }">
                选择文件
              </button>
            </label>
            <div v-if="loading" class="mt-6 flex items-center gap-2 text-primary text-sm font-medium">
              <span class="loading loading-spinner loading-sm"></span> {{ $t('extraction.uploading') }}
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：结果展示区 -->
      <div class="w-full md:w-7/12 bg-white rounded-2xl shadow-sm border border-[#dadce0] flex flex-col overflow-hidden">
        <div class="px-6 py-4 border-b border-[#f1f3f4] font-medium text-lg text-[#3c4043] flex items-center justify-between bg-white">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            抽取结果
          </div>
          <div v-if="result" class="badge badge-success gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            入库成功
          </div>
        </div>

        <div class="flex-1 overflow-auto p-6 bg-base-200/20">
          <div v-if="!result" class="h-full flex flex-col items-center justify-center opacity-50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            <p>{{ $t('extraction.noResultHint') }}</p>
          </div>

          <div v-else class="space-y-6">
            <!-- 统计标签 -->
            <div class="stats shadow w-full">
              <div class="stat place-items-center">
                <div class="stat-title">{{ $t('extraction.entitiesExtracted') }}</div>
                <div class="stat-value text-primary">{{ result.entities_count !== undefined ? result.entities_count : result.data?.entities?.length || 0 }}</div>
              </div>
              <div class="stat place-items-center">
                <div class="stat-title">{{ $t('extraction.relationsExtracted') }}</div>
                <div class="stat-value text-secondary">{{ result.relations_count !== undefined ? result.relations_count : result.data?.relations?.length || 0 }}</div>
              </div>
            </div>

            <!-- 实体列表 -->
            <div>
              <div class="divider text-sm font-medium text-base-content/50">实体列表</div>
              <div class="overflow-x-auto bg-base-100 rounded-box border border-base-200 shadow-sm max-h-60">
                <table class="table table-pin-rows table-pin-cols table-sm">
                  <thead>
                    <tr>
                      <th>实体名称</th>
                      <th>实体类型</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(entity, idx) in result.data.entities" :key="idx">
                      <td class="font-medium">{{ entity.name }}</td>
                      <td><div class="badge badge-outline badge-sm">{{ entity.type }}</div></td>
                    </tr>
                    <tr v-if="!result.data.entities?.length">
                      <td colspan="2" class="text-center py-4 opacity-50">无实体数据</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 关系列表 -->
            <div>
              <div class="divider text-sm font-medium text-base-content/50">关系列表</div>
              <div class="overflow-x-auto bg-base-100 rounded-box border border-base-200 shadow-sm max-h-60">
                <table class="table table-pin-rows table-pin-cols table-sm">
                  <thead>
                    <tr>
                      <th>{{ $t('extraction.source') }}</th>
                      <th>{{ $t('extraction.relationType') }}</th>
                      <th>{{ $t('extraction.target') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(relation, idx) in result.data.relations" :key="idx">
                      <td>{{ relation.source }}</td>
                      <td><div class="badge badge-warning badge-sm">{{ relation.type }}</div></td>
                      <td>{{ relation.target }}</td>
                    </tr>
                    <tr v-if="!result.data.relations?.length">
                      <td colspan="3" class="text-center py-4 opacity-50">无关系数据</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const inputText = ref('');
const loading = ref(false);
const result = ref<any>(null);
const activeTab = ref('text');

const onFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  loading.value = true;
  result.value = null;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('/api/ai/extract/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    result.value = response.data;
    // Reset file input so same file can be selected again
    target.value = '';
  } catch (error: any) {
    console.error(error);
    alert(error.response?.data?.detail || '文件处理失败');
  } finally {
    loading.value = false;
  }
};

const handleExtract = async () => {
  if (!inputText.value.trim()) {
    alert('请输入文本内容');
    return;
  }

  loading.value = true;
  result.value = null;

  try {
    const response = await axios.post('/api/ai/extract', {
      text: inputText.value
    });

    result.value = response.data;
  } catch (error: any) {
    console.error('抽取失败:', error);
    const msg = error.response?.data?.detail || '请求失败，请检查后端服务';
    alert(msg);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tailwind CSS and DaisyUI handles layout */
</style>
