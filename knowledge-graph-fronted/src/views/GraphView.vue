<template>
  <div class="graph-container">
    <div class="header">
      <h2>🕸️ 知识图谱可视化</h2>
      <p class="subtitle">直观展示实体与关系，支持交互式探索与查询</p>
    </div>

    <div class="content">
      <el-card class="box-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>📊 实体关系图</span>
            <el-button type="primary" @click="fetchGraphData" :loading="loading" circle>
              🔄
            </el-button>
          </div>
        </template>
        <div v-loading="loading" class="chart-wrapper">
          <div ref="chartRef" class="chart"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';
import { ElMessage } from 'element-plus';

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
    const response = await axios.get('http://localhost:8000/api/graph/data?limit=100');
    const data: GraphData = response.data;
    renderChart(data);
    ElMessage.success('图谱数据加载成功');
  } catch (error) {
    console.error('获取图谱数据失败:', error);
    ElMessage.error('获取图谱数据失败，请检查后端服务');
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
    value: link.type,
    label: {
      show: true,
      formatter: link.type
    }
  }));

  const option: echarts.EChartsOption = {
    title: {
      text: '多模态知识图谱',
      subtext: `节点数: ${nodes.length} | 关系数: ${links.length}`,
      top: 'top',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          return `实体: ${params.name}<br/>类型: ${params.value}`;
        } else {
          return `关系: ${params.value}<br/>${params.data.source} -> ${params.data.target}`; // 注意：这里source/target可能是ID，显示可能不直观，后续可优化
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
.graph-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.header {
  padding: 15px 20px;
  background: white;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.subtitle {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.content {
  flex: 1;
  padding: 20px;
  overflow: hidden;
}

.box-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.el-card__body) {
  flex: 1;
  position: relative;
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
