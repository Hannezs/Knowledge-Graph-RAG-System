<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute -top-10 -left-10 w-64 h-64 rounded-full bg-secondary opacity-20 blur-3xl"></div>
    <div class="absolute bottom-10 -right-10 w-72 h-72 rounded-full bg-primary opacity-20 blur-3xl"></div>

    <div class="card w-full max-w-sm shadow-2xl bg-base-100 z-10">
      <div class="card-body">
        <h2 class="text-2xl font-bold text-center text-primary mb-6 flex items-center justify-center gap-2">
          <span>📝</span> 注册新账号
        </h2>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-semibold">用户名</span></label>
            <input 
              v-model="registerForm.username" 
              type="text" 
              placeholder="最少3个字符" 
              class="input input-bordered w-full focus:input-primary transition-all" 
              required
              minlength="3"
            />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-semibold">密码</span></label>
            <input 
              v-model="registerForm.password" 
              type="password" 
              placeholder="最少6个字符" 
              class="input input-bordered w-full focus:input-primary transition-all" 
              required
              minlength="6"
            />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-semibold">确认密码</span></label>
            <input 
              v-model="registerForm.confirmPassword" 
              type="password" 
              placeholder="请再次输入密码" 
              class="input input-bordered w-full focus:input-primary transition-all" 
              required
              minlength="6"
            />
          </div>
          <div class="form-control mt-6">
            <button 
              type="submit" 
              class="btn btn-primary w-full shadow-lg shadow-primary/30"
              :disabled="loading"
            >
              <span v-if="loading" class="loading loading-spinner"></span>
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </div>
        </form>
        <div class="divider text-sm text-base-content/50">OR</div>
        <div class="text-center text-sm">
          <span class="text-base-content/70">已有账号？</span>
          <router-link to="/login" class="link link-primary font-semibold hover:text-primary-focus transition-colors">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from '../utils/message';
import axios from 'axios';

const router = useRouter();
const loading = ref(false);

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

const handleRegister = async () => {
  if (registerForm.password !== registerForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致！');
    return;
  }
  if (registerForm.username.length < 3) {
    ElMessage.error('用户名最少3个字符');
    return;
  }
  
  loading.value = true;
  try {
    await axios.post('/api/user/register', {
      username: registerForm.username,
      password: registerForm.password
    });

    ElMessage.success('注册成功，请登录');
    router.push('/login');
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
</style>
