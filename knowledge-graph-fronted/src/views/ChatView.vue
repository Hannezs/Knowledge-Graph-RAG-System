<template>
  <div class="chat-container">
    <div class="header">
      <h2>🤖 智能问答助手</h2>
      <p class="subtitle">基于知识库的 RAG 问答系统</p>
      <el-button v-if="sessionId" type="text" @click="clearHistory" class="clear-btn">
        🗑️ 清空对话
      </el-button>
    </div>

    <div class="chat-box" ref="chatBoxRef">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="avatar">
          {{ msg.role === 'user' ? '👤' : '🤖' }}
        </div>
        <div class="content">
          <div class="bubble">{{ msg.content }}</div>
          <div class="time">{{ msg.time }}</div>
        </div>
      </div>

      <div v-if="loading" class="message assistant">
        <div class="avatar">🤖</div>
        <div class="content">
          <div class="bubble loading">
            <span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
          </div>
        </div>
      </div>
    </div>

    <div class="input-area">
      <el-input
        v-model="inputQuery"
        placeholder="请输入您的问题..."
        @keyup.enter="handleSend"
        :disabled="loading"
      >
        <template #append>
          <el-button @click="handleSend" :loading="loading">发送</el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  time: string;
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '你好！我是智能问答助手，有什么可以帮你的吗？',
    time: new Date().toLocaleTimeString()
  }
]);

const inputQuery = ref('');
const loading = ref(false);
const chatBoxRef = ref<HTMLElement | null>(null);
const sessionId = ref<string | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatBoxRef.value) {
    chatBoxRef.value.scrollTop = chatBoxRef.value.scrollHeight;
  }
};

const clearHistory = () => {
  sessionId.value = null;
  messages.value = [{
    role: 'assistant',
    content: '对话已重置。有什么可以帮你的吗？',
    time: new Date().toLocaleTimeString()
  }];
};

const handleSend = async () => {
  const query = inputQuery.value.trim();
  if (!query) return;

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: query,
    time: new Date().toLocaleTimeString()
  });

  inputQuery.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await axios.post('http://localhost:8000/api/ai/chat', {
      query: query,
      session_id: sessionId.value
    });

    // 更新 session_id
    if (response.data.session_id) {
      sessionId.value = response.data.session_id;
    }

    // 添加助手回复
    messages.value.push({
      role: 'assistant',
      content: response.data.answer,
      time: new Date().toLocaleTimeString()
    });
  } catch (error) {
    console.error('问答失败:', error);
    messages.value.push({
      role: 'assistant',
      content: '抱歉，系统暂时无法回答您的问题，请稍后再试。',
      time: new Date().toLocaleTimeString()
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};
</script>

<style scoped>
.chat-container {
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
  position: relative;
}

.clear-btn {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.subtitle {
  font-size: 12px;
  color: #999;
  margin: 5px 0 0;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  gap: 10px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.assistant {
  align-self: flex-start;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #e0e0e0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.message.user .avatar {
  background: #409eff;
  color: white;
}

.message.assistant .avatar {
  background: #67c23a;
  color: white;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.bubble {
  padding: 10px 15px;
  border-radius: 10px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  line-height: 1.5;
  white-space: pre-wrap;
}

.message.user .bubble {
  background: #409eff;
  color: white;
  border-top-right-radius: 2px;
}

.message.assistant .bubble {
  background: white;
  border-top-left-radius: 2px;
}

.time {
  font-size: 12px;
  color: #999;
  align-self: flex-end;
}

.message.user .time {
  align-self: flex-start;
}

.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #eee;
}

.loading .dot {
  animation: blink 1.4s infinite both;
}

.loading .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0% { opacity: 0.2; }
  20% { opacity: 1; }
  100% { opacity: 0.2; }
}
</style>
