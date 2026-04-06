import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  time: string
}

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref<string | null>(null)
  const messages = ref<Message[]>([
    {
      role: 'assistant',
      content: '你好！我是智能问答助手，我已连接到核心知识库。您可以问我任何相关问题！',
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
    }
  ])

  function addMessage(msg: Message) {
    messages.value.push(msg)
  }

  function clearHistory(customInitialMessage?: string) {
    sessionId.value = null
    messages.value = [
      {
        role: 'assistant',
        content: customInitialMessage || '你好！我是智能问答助手，我已连接到核心知识库。您可以问我任何相关问题！',
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
      }
    ]
  }

  function setSessionId(id: string) {
    sessionId.value = id
  }

  return { sessionId, messages, addMessage, clearHistory, setSessionId }
})