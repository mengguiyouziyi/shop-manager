import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

// 需要认证的路由
const protectedRoutes = [
  '/dashboard',
  '/products',
  '/orders',
  '/members',
  '/categories',
  '/statistics',
  '/settings',
  '/pos'
]

// 公开路由
const publicRoutes = [
  '/login',
  '/register',
  '/forgot-password',
  '/'
]

export function useAuthMiddleware() {
  const authStore = useAuthStore()
  const router = useRouter()

  // 检查路由是否需要认证
  const isProtectedRoute = (path: string): boolean => {
    return protectedRoutes.some(route => path.startsWith(route))
  }

  // 检查路由是否公开
  const isPublicRoute = (path: string): boolean => {
    return publicRoutes.some(route => path === route || path.startsWith(route))
  }

  // 路由守卫
  const requireAuth = (to: any, from: any, next: any) => {
    const isAuthenticated = authStore.isAuthenticated
    const isProtected = isProtectedRoute(to.path)
    const isPublic = isPublicRoute(to.path)

    // 如果用户已认证且访问登录页，重定向到首页
    if (isAuthenticated && to.path === '/login') {
      next('/dashboard')
      return
    }

    // 如果需要认证但用户未认证，重定向到登录页
    if (isProtected && !isAuthenticated) {
      ElMessage.warning('请先登录')
      next('/login')
      return
    }

    // 如果用户已认证且访问公开页面，允许访问
    if (isAuthenticated && isPublic) {
      next()
      return
    }

    // 其他情况允许访问
    next()
  }

  // 自动刷新token
  const autoRefreshToken = async () => {
    if (authStore.token) {
      try {
        // 这里可以实现token刷新逻辑
        // 暂时只是检查token是否有效
        const isValid = await checkTokenValidity()
        if (!isValid) {
          authStore.logout()
          router.push('/login')
        }
      } catch (error) {
        console.error('Token验证失败:', error)
        authStore.logout()
        router.push('/login')
      }
    }
  }

  // 检查token有效性
  const checkTokenValidity = async (): Promise<boolean> => {
    try {
      // 这里可以调用后端API验证token
      // 暂时返回true，实际应该调用验证接口
      return true
    } catch (error) {
      return false
    }
  }

  // 设置定时器定期检查token
  const setupTokenRefresh = () => {
    // 每5分钟检查一次token
    setInterval(autoRefreshToken, 5 * 60 * 1000)
  }

  return {
    requireAuth,
    isProtectedRoute,
    isPublicRoute,
    autoRefreshToken,
    setupTokenRefresh
  }
}
