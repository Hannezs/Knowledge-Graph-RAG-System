export default {
  nav: {
    home: '首页',
    graph: '构建图谱',
    extraction: '知识抽取',
    chat: 'AI 问答',
    currentUser: '当前账户',
    logout: '退出登录',
    language: '语言'
  },
  home: {
    welcome: '欢迎使用',
    kgSystem: '知识图谱系统',
    description: '基于大模型与图数据库的新一代知识管理平台，带您轻松探索实体与关系网络。',
    features: {
      graph: {
        title: '知识图谱可视化',
        desc: '直观展示实体与关系，支持交互式探索与查询'
      },
      extraction: {
        title: '智能知识抽取',
        desc: '上传文档或输入文本，自动提取知识并入库'
      },
      chat: {
        title: 'RAG 智能问答',
        desc: '基于知识库的精准问答，支持多轮对话'
      }
    }
  },
  chat: {
    title: 'AI 问答助手',
    poweredBy: 'Powered by Knowledge Graph RAG',
    clearHistory: '清除记忆',
    you: 'You',
    assistant: 'AI Assistant',
    thinking: 'AI 思考中...',
    placeholder: '问我任何关于知识库的问题...',
    disclaimer: 'AI 可能会提供不准确的信息，请核实重要内容。'
  },
  extraction: {
    title: '知识抽取与入库',
    desc: '支持文本输入或文件上传，AI将自动提取实体与关系并存入图数据库',
    dataSource: '数据来源',
    textInput: '文本输入',
    fileUpload: '文件上传',
    clickToUpload: '点击选择文件上传',
    uploadHints: '支持 PDF, Excel, CSV, TXT 文件',
    uploading: '正在解析文件并抽取知识...',
    textPlaceholder: '请输入需要进行知识抽取的文本内容...',
    confirmExtract: '马上抽取知识入库',
    resultTitle: '分析提取结果',
    extractSuccess: '提取成功',
    noResultHint: '暂无抽取结果，请在左侧输入数据并开始抽取',
    entitiesExtracted: '提取实体数',
    relationsExtracted: '提取关系数',
    detailEntities: '提取到的实体',
    detailRelations: '提取到的关系',
    source: '源实体',
    relationType: '关系类型',
    target: '目标实体'
  },
  graph: {
    title: '知识图谱浏览器',
    desc: '直观展示实体与关系，支持交互式探索与查询',
    poweredBy: '基于 Milvus & PostgreSQL 驱动',
    refresh: '刷新图谱',
    loading: '加载中...',
    nodes: '节点',
    links: '边',
    noData: '暂无图谱数据',
    chartTitle: '多模态知识图谱',
    chartSubtext: '节点数: {nodes} | 关系数: {links}',
    tooltipEntity: '实体: {name}<br/>类型: {value}',
    tooltipRelation: '关系: {value}<br/>{source} -> {target}'
  }
}
