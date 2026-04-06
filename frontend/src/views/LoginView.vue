<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute -top-10 -right-10 w-64 h-64 rounded-full bg-primary opacity-20 blur-3xl"></div>
    <div class="absolute bottom-10 -left-10 w-72 h-72 rounded-full bg-secondary opacity-20 blur-3xl"></div>

    <div class="card w-full max-w-sm shadow-2xl bg-base-100 z-10">
      <div class="card-body">
        <h2 class="text-2xl font-bold text-center text-primary mb-6 flex items-center justify-center gap-2">
          <span>🔐</span> 欢迎登录
        </h2>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-semibold">用户名</span></label>
            <input 
              v-model="loginForm.username" 
              type="text" 
              placeholder="请输入用户名" 
              class="input input-bordered w-full focus:input-primary transition-all" 
              required
            />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-semibold">密码</span></label>
            <input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码" 
              class="input input-bordered w-full focus:input-primary transition-all" 
              required
            />
          </div>
          <div class="form-control mt-6">
            <button 
              type="submit" 
              class="btn btn-primary w-full shadow-lg shadow-primary/30"
              :disabled="loading"
            >
              <span v-if="loading" class="loading loading-spinner"></span>
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
        </form>
        <div class="divider text-sm text-base-content/50">OR</div>
        <div class="text-center text-sm">
          <span class="text-base-content/70">还没有账号？</span>
          <router-link to="/register" class="link link-primary font-semibold hover:text-primary-focus transition-colors">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from '../utils/message';
import { useUserStore } from '../stores/user';
import axios from 'axios';

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

const loginForm = reactive({
  username: '',
  password: ''
});

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码');
    return;
  }
  loading.value = true;
  try {
    const params = new URLSearchParams();
    params.append('username', loginForm.username);
    params.append('password', loginForm.password);

    const response = await axios.post('/api/user/login', params);

    const { access_token } = response.data;
    userStore.setLoginInfo(access_token, loginForm.username);

    ElMessage.success('登录成功');
    router.push('/');
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 使用 Tailwind 即可，不再需要自定义大量 CSS */
</style>
