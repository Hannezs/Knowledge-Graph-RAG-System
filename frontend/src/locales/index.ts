import { createI18n } from 'vue-i18n'
import zh from './zh'
import en from './en'

// 获取浏览器默认语言或者从 localStorage 中读取已选语言
const defaultLanguage = localStorage.getItem('language') || navigator.language.split('-')[0] || 'zh'
const currentLang = ['zh', 'en'].includes(defaultLanguage) ? defaultLanguage : 'zh'

const i18n = createI18n({
  locale: currentLang,
  fallbackLocale: 'en',
  legacy: false, // 适配 vue3 composition API
  messages: {
    zh,
    en
  }
})

export default i18n
