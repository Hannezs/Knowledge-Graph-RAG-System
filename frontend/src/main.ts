import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './locales'
import { ElMessage } from './utils/message'
import './index.css'
import axios from 'axios'

import { useUserStore } from './stores/user'

// 全局 Axios 配置与拦截器
axios.defaults.baseURL = '' // Vite 代理已配置 /api 前缀，因此留空走同源相对路径即可
axios.interceptors.request.use(config => {
  const userStore = useUserStore()
  const token = userStore.token
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  response => response,
  error => {
    // 统一错误处理
    if (error.response?.status === 401) {
      const userStore = useUserStore()
      ElMessage.error('登录失效或未登录，请重新登录')
      userStore.logout()
      router.push('/login')
    } else if (error.response?.status >= 500) {
      ElMessage.error(error.response?.data?.detail || '服务器内部错误，请稍后重试')
    } else if (error.response?.status >= 400) {
      ElMessage.error(error.response?.data?.detail || '请求失败')
    } else {
      ElMessage.error('网络出现异常，无法连接服务')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

app.mount('#app')
