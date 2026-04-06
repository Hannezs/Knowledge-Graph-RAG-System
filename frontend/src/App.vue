

<template>
  <div class="app-container min-h-screen bg-base-200">
    <div class="navbar bg-base-100 shadow-sm border-b border-gray-200 px-6" v-if="!isAuthPage">
      <div class="flex-1">
        <a class="btn btn-ghost text-xl font-[500] text-[#5f6368] hover:bg-transparent">
          <span class="mr-2 text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </span>
          <span class="text-xl font-[Product Sans,sans-serif]">KG System</span>
        </a>
      </div>
      <div class="flex-none gap-2">
        <ul class="menu menu-horizontal px-1 font-medium text-sm text-[#5f6368]">
          <li><router-link to="/" active-class="text-primary bg-primary/10 rounded-full">{{ $t('nav.home') }}</router-link></li>
          <li><router-link to="/graph" active-class="text-primary bg-primary/10 rounded-full">{{ $t('nav.graph') }}</router-link></li>
          <li><router-link to="/extraction" active-class="text-primary bg-primary/10 rounded-full">{{ $t('nav.extraction') }}</router-link></li>
          <li><router-link to="/chat" active-class="text-primary bg-primary/10 rounded-full">{{ $t('nav.chat') }}</router-link></li>
        </ul>
        
        <!-- Language Selector -->
        <div class="dropdown dropdown-end ml-2">
          <label tabindex="0" class="btn btn-ghost btn-circle text-[#5f6368]">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
            </svg>
          </label>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-base-100 rounded-box w-32 border border-gray-100">
            <li><a :class="{ 'active bg-primary/10 text-primary': currentLang === 'zh' }" @click="switchLanguage('zh')">中文</a></li>
            <li><a :class="{ 'active bg-primary/10 text-primary': currentLang === 'en' }" @click="switchLanguage('en')">English</a></li>
          </ul>
        </div>

        <div class="dropdown dropdown-end ml-2">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar tooltip tooltip-bottom tooltip-primary" :data-tip="userStore.username">
            <div class="w-10 rounded-full bg-primary text-primary-content flex items-center justify-center font-medium shadow-sm">
              <span class="text-sm">{{ userStore.username.slice(0, 1).toUpperCase() }}</span>
            </div>
          </label>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-3 shadow-lg bg-base-100 rounded-box w-56 border border-gray-100">
            <li class="menu-title text-xs text-gray-500 font-normal px-2 mb-1">{{ $t('nav.currentUser') }}</li>
            <li class="px-2 mb-2 font-medium text-gray-800">{{ userStore.username }}</li>
            <div class="divider my-0"></div>
            <li><a @click="handleCommand('logout')" class="text-error hover:bg-error/10 hover:text-error rounded-md mt-1">{{ $t('nav.logout') }}</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="main-content flex-1 max-w-[1400px] w-full mx-auto p-4 md:p-6 lg:p-8">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router'
import { ElMessage } from './utils/message'
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from './stores/user'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const currentLang = ref(locale.value)

const switchLanguage = (lang: string) => {
  locale.value = lang
  currentLang.value = lang
  localStorage.setItem('language', lang)
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const activeIndex = computed(() => route.path)

const isAuthPage = computed(() => {
  return ['/login', '/register'].includes(route.path)
})

onMounted(() => {
  // 简单从localStorage获取用户名，实际项目中可能需要从后端获取用户信息
  // 这里假设登录时保存了用户名，或者解析token获取
  // 暂时用默认值
})

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout();
    ElMessage.success('已退出登录');
    router.push('/login');
  }
}
</script>

<style>
/* 全局样式重置 */
body {
  margin: 0;
  font-family: 'Product Sans', 'Roboto', 'Helvetica Neue', Helvetica, 'PingFang SC', sans-serif;
  background-color: #f8f9fa; /* Google Gray Surface */
}

/* Scrollbar styling for Google feel */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent; 
}
::-webkit-scrollbar-thumb {
  background: #dadce0; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #bdc1c6; 
}
</style>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  position: relative;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
