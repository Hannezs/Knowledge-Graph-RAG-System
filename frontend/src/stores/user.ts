import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const username = ref<string>(localStorage.getItem('username') || 'User')

  function setLoginInfo(newToken: string, newUsername: string = 'User') {
    token.value = newToken
    username.value = newUsername
    localStorage.setItem('token', newToken)
    localStorage.setItem('username', newUsername)
  }

  function logout() {
    token.value = null
    username.value = 'User'
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, setLoginInfo, logout }
})