// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
// 导入刚才创建的HomeView
import HomeView from '../views/HomeView.vue'
import GraphView from '../views/GraphView.vue'
import ExtractionView from '../views/ExtractionView.vue'
import ChatView from '../views/ChatView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // 首页路径
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/graph',
      name: 'graph',
      component: GraphView,
      meta: { requiresAuth: true }
    },
    {
      path: '/extraction',
      name: 'extraction',
      component: ExtractionView,
      meta: { requiresAuth: true }
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/');
  } else {
    next();
  }
});

export default router
