import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 状态
  const appName = ref('店铺管理系统')
  const version = ref('1.0.0')
  const lastUpdate = ref(new Date().toLocaleString('zh-CN'))
  const isLoading = ref(false)
  const notifications = ref<string[]>([])
  
  // 用户认证状态
  const user = ref<any>(null)
  const isAuthenticated = computed(() => !!user.value)

  // 计算属性
  const appInfo = computed(() => ({
    name: appName.value,
    version: version.value,
    lastUpdate: lastUpdate.value
  }))

  const hasNotifications = computed(() => notifications.value.length > 0)

  // 方法
  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  const addNotification = (message: string) => {
    notifications.value.push(message)
    // 5秒后自动移除
    setTimeout(() => {
      removeNotification(message)
    }, 5000)
  }

  const removeNotification = (message: string) => {
    const index = notifications.value.indexOf(message)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  const updateAppInfo = () => {
    lastUpdate.value = new Date().toLocaleString('zh-CN')
  }

  // 用户认证方法
  const setUser = (userData: any) => {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('rememberedUser')
    addNotification('您已成功退出登录')
  }

  const loadUserFromStorage = () => {
    try {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        user.value = JSON.parse(savedUser)
      }
    } catch (error) {
      console.error('Failed to load user from storage:', error)
      localStorage.removeItem('user')
    }
  }

  // 初始化时加载用户状态
  loadUserFromStorage()

  return {
    // 状态
    appName,
    version,
    lastUpdate,
    isLoading,
    notifications,
    user,
    isAuthenticated,
    
    // 计算属性
    appInfo,
    hasNotifications,
    
    // 方法
    setLoading,
    addNotification,
    removeNotification,
    clearNotifications,
    updateAppInfo,
    setUser,
    logout,
    loadUserFromStorage
  }
})
