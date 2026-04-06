<template>
  <div class="min-h-screen bg-transparent p-4 md:p-8">
    <div class="max-w-6xl mx-auto space-y-12 mt-4">
      <!-- 欢迎区域 -->
      <div class="text-center py-10 space-y-3">
        <div class="inline-flex justify-center items-center mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-primary mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          <h1 class="text-4xl md:text-5xl font-normal text-[#1f1f1f] tracking-tight font-[Product Sans,sans-serif]">
            {{ $t('home.welcome') }} <span class="text-primary font-medium">{{ $t('home.kgSystem') }}</span>
          </h1>
        </div>
        <p class="text-lg text-[#5f6368] font-[400] max-w-2xl mx-auto">
          {{ $t('home.description') }}
        </p>
      </div>

      <!-- 功能卡片区 (Material Cards) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          v-for="feature in features" 
          :key="feature.path"
          @click="$router.push(feature.path)"
          class="card bg-white shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer border border-[#dadce0] rounded-2xl overflow-hidden"
        >
          <div class="card-body p-6 pb-8">
            <div class="text-primary mb-4" v-html="feature.iconSVG"></div>
            <h2 class="card-title text-xl font-medium text-[#202124]">{{ $t(feature.titleKey) }}</h2>
            <p class="text-[#5f6368] mt-1 text-sm leading-relaxed">{{ $t(feature.descKey) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const features = computed(() => [
  {
    titleKey: 'home.features.graph.title',
    descKey: 'home.features.graph.desc',
    iconSVG: `<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>`,
    path: '/graph'
  },
  {
    titleKey: 'home.features.extraction.title',
    descKey: 'home.features.extraction.desc',
    iconSVG: `<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>`,
    path: '/extraction'
  },
  {
    titleKey: 'home.features.chat.title',
    descKey: 'home.features.chat.desc',
    iconSVG: `<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>`,
    path: '/chat'
  }
]);
</script>

<style scoped>
/* Tailwind CSS and DaisyUI handles layout */
</style>
