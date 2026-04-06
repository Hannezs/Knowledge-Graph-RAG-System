<template>
  <div class="h-[calc(100vh-100px)] flex flex-col bg-white rounded-2xl shadow-sm border border-[#dadce0] overflow-hidden max-w-5xl mx-auto my-2">
    <!-- Header -->
    <div class="bg-white px-6 py-4 flex justify-between items-center border-b border-[#f1f3f4] z-10">
      <div>
        <h2 class="text-xl font-normal text-[#202124] flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          {{ $t('chat.title') }}
        </h2>
        <p class="text-xs text-[#5f6368] mt-1 pr-1 font-medium flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-primary/70" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
          </svg>
          {{ $t('chat.poweredBy') }}
        </p>
      </div>
      <button 
        v-if="sessionId" 
        @click="clearHistory" 
        class="btn btn-ghost btn-sm text-[#5f6368] hover:bg-[#f1f3f4] rounded-full font-medium"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
        {{ $t('chat.clearHistory') }}
      </button>
    </div>

    <!-- Chat Box -->
    <div class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 bg-transparent" ref="chatBoxRef">
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <div class="flex gap-3 max-w-[85%]" :class="[msg.role === 'user' ? 'flex-row-reverse' : 'flex-row']">
          <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-medium mt-1 shadow-sm" :class="[msg.role === 'user' ? 'bg-primary text-white' : 'bg-white border border-[#dadce0] text-primary']">
            <span v-if="msg.role === 'user'">U</span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <div class="flex flex-col" :class="[msg.role === 'user' ? 'items-end' : 'items-start']">
            <div class="text-xs text-[#5f6368] mb-1 px-1">
              {{ msg.role === 'user' ? $t('chat.you') : $t('chat.assistant') }}
              <time class="opacity-70 ml-2 font-mono">{{ msg.time }}</time>
            </div>
            <div 
              :class="['px-5 py-3 rounded-2xl text-[15px] leading-relaxed whitespace-pre-wrap', 
                msg.role === 'user' ? 'bg-[#e8f0fe] text-[#1a73e8] rounded-tr-sm' : 'bg-[#f1f3f4] text-[#202124] rounded-tl-sm border border-[#dadce0]/50']"
            >{{ msg.content }}</div>
          </div>
        </div>
      </div>

      <!-- Loading Indicator -->
      <div v-if="loading" class="flex justify-start">
        <div class="flex gap-3 max-w-[80%] flex-row">
          <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-medium mt-1 bg-white border border-[#dadce0] text-primary shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <div class="flex flex-col items-start">
            <div class="text-xs text-[#5f6368] mb-1 px-1">{{ $t('chat.assistant') }}</div>
            <div class="px-5 py-3 rounded-2xl bg-[#f1f3f4] text-[#202124] rounded-tl-sm border border-[#dadce0]/50 flex items-center h-[48px] gap-2">
              <span class="loading loading-dots loading-sm text-[#5f6368]"></span>
              <span class="text-sm text-[#5f6368]">{{ $t('chat.thinking') }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-white p-4 border-t border-[#f1f3f4] z-10 pb-6">
      <div class="w-full px-2 max-w-4xl mx-auto flex items-end gap-2 bg-[#f1f3f4] rounded-[24px] px-2 py-2 border border-transparent focus-within:border-primary/30 focus-within:bg-white focus-within:shadow-md transition-all duration-300">
        <textarea 
          v-model="inputQuery"
          @keyup.enter.exact.prevent="handleSend"
          :disabled="loading"
          class="textarea bg-transparent border-none flex-1 focus:outline-none min-h-[44px] max-h-[120px] resize-none text-[15px] py-3 text-[#202124] placeholder:text-[#5f6368]" 
          :placeholder="$t('chat.placeholder')" 
          rows="1"
        ></textarea>
        <button 
          @click="handleSend" 
          :disabled="loading || !inputQuery.trim()"
          class="btn btn-circle btn-primary btn-sm mb-1 mr-1 disabled:bg-transparent disabled:text-gray-400"
        >
          <span v-if="loading" class="loading loading-spinner loading-xs"></span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 ml-0.5">
            <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
          </svg>
        </button>
      </div>
      <div class="text-center mt-2 text-[11px] text-[#5f6368]">
        {{ $t('chat.disclaimer') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { useChatStore } from '../stores/chat';
import { storeToRefs } from 'pinia';
import axios from 'axios';

const chatStore = useChatStore();
const { messages, sessionId } = storeToRefs(chatStore);

const inputQuery = ref('');
const loading = ref(false);
const chatBoxRef = ref<HTMLElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatBoxRef.value) {
    chatBoxRef.value.scrollTop = chatBoxRef.value.scrollHeight;
  }
};

const clearHistory = () => {
  chatStore.clearHistory('对话记忆已清除。我们重新开始吧！');
};

const handleSend = async () => {
  const query = inputQuery.value.trim();
  if (!query) return;

  // Add User Message
  messages.value.push({
    role: 'user',
    content: query,
    time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
  });

  inputQuery.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: query,
        session_id: sessionId.value
      })
    });

    if (!response.ok) throw new Error('网络请求失败');
    
    loading.value = false;
    const msgIndex = messages.value.length;
    messages.value.push({
      role: 'assistant',
      content: '',
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;
    let buffer = '';

    while (reader && !done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;
      if (value) {
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep the last incomplete line
        
        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.slice(5).trim();
            if (dataStr === '[DONE]') {
              done = true;
              break;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.session_id) sessionId.value = data.session_id;
              if (data.chunk) {
                const msg = messages.value[msgIndex];
                if (msg) {
                  msg.content += data.chunk;
                }
                scrollToBottom();
              }
            } catch (e) {
              // Ignore incomplete JSON chunks (rare)
            }
          }
        }
      }
    }
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '请求出错，请稍后重新尝试。',
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};
</script>

<style scoped>
/* 无需手写复杂CSS，全面依赖Tailwind/DaisyUI */

</style>
