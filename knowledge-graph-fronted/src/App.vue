

<template>
  <div class="app-container">
    <el-header class="app-header" v-if="!isAuthPage">
      <div class="logo">
        <span class="logo-icon">🧠</span>
        <span class="logo-text">知识图谱智能系统</span>
      </div>
      <el-menu
        :default-active="activeIndex"
        class="nav-menu"
        mode="horizontal"
        router
        :ellipsis="false"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/graph">知识图谱</el-menu-item>
        <el-menu-item index="/extraction">知识抽取</el-menu-item>
        <el-menu-item index="/chat">智能问答</el-menu-item>
      </el-menu>

      <div class="user-actions">
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="32" :icon="UserFilled" />
            <span class="username">{{ username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <div class="main-content">
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
import { ElMenu, ElMenuItem, ElHeader, ElDropdown, ElDropdownMenu, ElDropdownItem, ElAvatar, ElIcon, ElMessage } from 'element-plus'
import { UserFilled, ArrowDown } from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import { computed, ref, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const activeIndex = computed(() => route.path)

const isAuthPage = computed(() => {
  return ['/login', '/register'].includes(route.path)
})

const username = ref('User')

onMounted(() => {
  // 简单从localStorage获取用户名，实际项目中可能需要从后端获取用户信息
  // 这里假设登录时保存了用户名，或者解析token获取
  // 暂时用默认值
})

const handleCommand = (command: string) => {
  if (command === 'logout') {
    localStorage.removeItem('token');
    ElMessage.success('已退出登录');
    router.push('/login');
  }
}
</script>

<style>
/* 全局样式重置 */
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f0f2f5;
}
</style>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 0 40px;
  z-index: 10;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
}

.logo-icon {
  font-size: 24px;
}

.nav-menu {
  border-bottom: none;
  flex: 1;
  justify-content: center; /* 菜单居中 */
  background: transparent;
}

.user-actions {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  color: #606266;
}

.username {
  margin: 0 8px;
  font-size: 14px;
}

.main-content {
  flex: 1;
  overflow: hidden; /* 防止双重滚动条 */
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
