export default {
  nav: {
    home: 'Home',
    graph: 'Graph View',
    extraction: 'Extraction',
    chat: 'AI Chat',
    currentUser: 'Current User',
    logout: 'Sign out',
    language: 'Language'
  },
  home: {
    welcome: 'Welcome to',
    kgSystem: 'KG System',
    description: 'Explore entities and relationships effortlessly with our next-generation knowledge management platform powered by LLMs and Graph databases.',
    features: {
      graph: {
        title: 'Graph Visualization',
        desc: 'Visually display entities and relationships, supporting interactive exploration and queries.'
      },
      extraction: {
        title: 'Smart Extraction',
        desc: 'Upload documents or text to automatically extract and store knowledge.'
      },
      chat: {
        title: 'RAG AI Assistant',
        desc: 'Accurate Q&A based on your knowledge base, supporting multi-turn conversations.'
      }
    }
  },
  chat: {
    title: 'AI Assistant',
    poweredBy: 'Powered by Knowledge Graph RAG',
    clearHistory: 'Clear History',
    you: 'You',
    assistant: 'AI Assistant',
    thinking: 'AI is thinking...',
    placeholder: 'Ask me anything about the knowledge base...',
    disclaimer: 'AI may provide inaccurate information. Please verify important content.'
  },
  extraction: {
    title: 'Knowledge Extraction',
    desc: 'Support text input or file upload. AI will auto-extract entities and store relations to Graph DB',
    dataSource: 'Data Source',
    textInput: 'Text Input',
    fileUpload: 'File Upload',
    clickToUpload: 'Click to select a file',
    uploadHints: 'Supports PDF, Excel, CSV, TXT files',
    uploading: 'Analyzing file and extracting knowledge...',
    textPlaceholder: 'Please enter the text for knowledge extraction...',
    confirmExtract: 'Extract and Store Knowledge',
    resultTitle: 'Extraction Results',
    extractSuccess: 'Extraction Successful',
    noResultHint: 'No extraction results. Please input data on the left to begin.',
    entitiesExtracted: 'Entities Extracted',
    relationsExtracted: 'Relations Extracted',
    detailEntities: 'Extracted Entities',
    detailRelations: 'Extracted Relations',
    source: 'Source',
    relationType: 'Relation Type',
    target: 'Target'
  },
  graph: {
    title: 'Knowledge Graph Browser',
    desc: 'Visually display entities and relationships, supporting interactive exploration and queries.',
    poweredBy: 'Powered by Milvus & PostgreSQL',
    refresh: 'Refresh Graph',
    loading: 'Loading...',
    nodes: 'Nodes',
    links: 'Edges',
    noData: 'No graph data available',
    chartTitle: 'Multimodal Knowledge Graph',
    chartSubtext: 'Nodes: {nodes} | Edges: {links}',
    tooltipEntity: 'Entity: {name}<br/>Type: {value}',
    tooltipRelation: 'Relation: {value}<br/>{source} -> {target}'
  }
}
