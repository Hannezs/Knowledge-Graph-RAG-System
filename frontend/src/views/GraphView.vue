<template>
  <div class="h-[calc(100vh-100px)] flex flex-col bg-transparent p-0 md:p-2">
    <div class="mb-4 flex flex-col px-2">
      <h2 class="text-2xl font-normal text-[#202124] flex items-center gap-2 tracking-tight">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        知识图谱可视化
      </h2>
      <p class="text-sm text-[#5f6368] mt-1">{{ t('graph.desc') }}</p>
    </div>

    <div class="flex-1 bg-white rounded-2xl shadow-sm border border-[#dadce0] overflow-hidden flex flex-col">
      <div class="px-6 py-4 border-b border-[#f1f3f4] flex justify-between items-center bg-white">
        <span class="font-medium text-lg text-[#3c4043] flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          实体关系图
        </span>
        <button 
          @click="fetchGraphData" 
          :disabled="loading" 
          class="btn btn-primary btn-sm gap-2 px-4 shadow-none hover:shadow-md transition-shadow rounded-full font-medium"
        >
          <span v-if="loading" class="loading loading-spinner loading-xs"></span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          重新加载
        </button>
      </div>
      <div class="flex-1 relative">
        <div v-if="loading" class="absolute inset-0 bg-base-100/50 z-10 flex items-center justify-center">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>
        <div ref="chartRef" class="w-full h-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import * as echarts from 'echarts';
import axios from 'axios';

const { t } = useI18n();

// 定义数据接口
interface GraphNode {
  id: string;
  name: string;
  type: string;
}

interface GraphLink {
  id: string;
  source: string;
  target: string;
  type: string;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

const chartRef = ref<HTMLElement | null>(null);
let myChart: echarts.ECharts | null = null;
const loading = ref(false);

// 初始化图表
const initChart = () => {
  if (chartRef.value) {
    myChart = echarts.init(chartRef.value);
    window.addEventListener('resize', resizeChart);
  }
};

const resizeChart = () => {
  myChart?.resize();
};

// 获取数据并渲染
const fetchGraphData = async () => {
  loading.value = true;
  try {
    const response = await axios.get('/api/graph/data?limit=100');
    const data: GraphData = response.data;
    renderChart(data);
  } catch (error) {
    console.error('获取图谱数据失败:', error);
  } finally {
    loading.value = false;
  }
};

// 渲染图表
const renderChart = (data: GraphData) => {
  if (!myChart) return;

  // 提取所有实体类型作为图例分类
  const categories = Array.from(new Set(data.nodes.map(node => node.type))).map(type => ({ name: type }));

  // 转换节点数据
  const nodes = data.nodes.map(node => ({
    id: node.id,
    name: node.name,
    value: node.type,
    category: data.nodes.findIndex(n => n.type === node.type) % categories.length, // 简单映射分类索引
    symbolSize: 30,
    label: {
      show: true
    }
  }));

  // 转换边数据
  const links = data.links.map(link => ({
    source: link.source,
    target: link.target,
    name: link.type, // ECharts Edge name can be a string
    label: {
      show: true,
      formatter: link.type
    }
  }));

  const option: echarts.EChartsOption = {
    title: {
      text: t('graph.chartTitle'),
      subtext: t('graph.chartSubtext', { nodes: nodes.length, links: links.length }),
      top: 'top',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          return t('graph.tooltipEntity', { name: params.name, value: params.value });
        } else {
          return t('graph.tooltipRelation', { value: params.value, source: params.data.source, target: params.data.target }); // 注意：这里source/target可能是ID，显示可能不直观，后续可优化
        }
      }
    },
    legend: {
      data: categories.map(c => c.name),
      bottom: 10
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: links,
        categories: categories,
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}'
        },
        force: {
          repulsion: 300,
          edgeLength: 100
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  };

  myChart.setOption(option);
};

onMounted(() => {
  initChart();
  fetchGraphData();
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart);
  myChart?.dispose();
});
</script>

<style scoped>
/* Tailwind CSS and DaisyUI handles layout */
</style>
