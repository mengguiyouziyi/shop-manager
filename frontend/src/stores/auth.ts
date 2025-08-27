import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, Shop, LoginCredentials } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const shop = ref<Shop | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authApi.login(credentials)
      
      // Python后端返回格式: {access_token, token_type, user}
      if (response.access_token) {
        const { access_token: authToken, user: userData } = response
        
        token.value = authToken
        user.value = {
          ...userData,
          created_at: userData.created_at || new Date().toISOString()
        }
        shop.value = { id: 1, name: '默认店铺', status: 1 }
        
        localStorage.setItem('token', authToken)
        localStorage.setItem('user', JSON.stringify(userData))
        
        return response
      } else {
        throw new Error('登录失败')
      }
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    shop.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const loadUserFromStorage = () => {
    try {
      const savedToken = localStorage.getItem('token')
      const savedUser = localStorage.getItem('user')
      
      if (savedToken && savedUser) {
        token.value = savedToken
        user.value = JSON.parse(savedUser)
        shop.value = user.value?.shop || { id: user.value?.shop_id || 1, name: '默认店铺', status: 1 }
      }
    } catch (error) {
      console.error('Failed to load user from storage:', error)
      // 清除无效的存储数据
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // 初始化时立即加载用户状态
  loadUserFromStorage()

  return {
    user,
    token,
    shop,
    isAuthenticated,
    login,
    logout,
    loadUserFromStorage
  }
})