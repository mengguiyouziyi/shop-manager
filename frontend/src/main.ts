import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './index.css' // 引入Tailwind CSS
import App from './App.vue'

// 创建简单的路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('./views/MinimalTest.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/simple',
      name: 'SimpleTest',
      component: () => import('./views/SimpleTest.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('./views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/products',
      name: 'ProductManagement',
      component: () => import('./views/ProductManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'OrderManagement',
      component: () => import('./views/OrderManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: () => import('./views/UserProfile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('./views/Login.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

const app = createApp(App)
const pinia = createPinia()

// 使用插件
app.use(pinia)
app.use(ElementPlus)
app.use(router)

// 路由守卫 - 在pinia初始化后设置
import { useAppStore } from './stores/app'

router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  
  if (to.meta.requiresAuth && !appStore.isAuthenticated) {
    // 需要认证但未登录，重定向到登录页
    next('/login')
  } else if (to.path === '/login' && appStore.isAuthenticated) {
    // 已登录用户访问登录页，重定向到首页
    next('/')
  } else {
    next()
  }
})

app.mount('#app')