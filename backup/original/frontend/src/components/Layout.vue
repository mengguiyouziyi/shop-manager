<template>
  <div class="layout">
    <!-- 新侧边栏组件 -->
    <Sidebar ref="sidebar" />
    
    <!-- 右侧主极内容区域 -->
    <div class="main-container">
      <!-- 顶部用户信息栏 -->
      <div class="top-header">
        <div class="header-content">
          <div class="breadcrumb">
            {{ breadcrumbText }}
          </div>
          
          <div class="user-info">
            <span class="username">测试用户</span>
            <button class="logout-btn" @click="logout">退出登录</button>
          </div>
        </div>
      </div>
      
      <!-- 主要内容区域 -->
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from './Layout/Sidebar.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const sidebar = ref<{ toggleCollapse: () => void; isCollapsed: boolean } | null>(null)

// 侧边栏折叠状态
const isCollapsed = ref(false)

// 面包屑文本
const breadcrumbText = computed(() => {
  const currentPath = route.path
  const routeName = route.name?.toString() || ''
  
  // 简单的路由到名称映射
  const routeMap: Record<string, string> = {
    'dashboard': '仪表盘',
    'products': '商品管理',
    'categories': '分类极管理',
    'orders': '订单管理',
    'members': '会员管理',
    'statistics': '数据统计',
    'settings': '系统设置',
    'users': '用户管理',
    'shops': '店铺管理',
    'profile': '个人资料',
    'pos': 'POS收银'
  }
  
  const currentName = routeMap[routeName] || '首页'
  return `首页 / ${currentName}`
})

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  if (sidebar.value) {
    sidebar.value.toggleCollapse()
    isCollapsed.value = !isCollapsed.value
  }
}

// 监听侧边栏折叠状态变化
onMounted(() => {
  // 初始化折叠状态
  if (sidebar.value) {
    isCollapsed.value = sidebar.value.isCollapsed
  }
})

// 退出登录
const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* 重置样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 主布局 */
.layout {
  height: 100vh;
  display: flex;
}

/* 右侧主内容区域 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部用户信息栏 */
.top-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 极4px rgba(0, 0, 0, 0.1);
  height: 60px;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.breadcrumb {
  font-size: 14px;
  color: #606266;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15极px;
}

.username {
  font-size: 14px;
  color: #606266;
}

.logout-btn {
  padding: 6px 12px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background: #e74c3c;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

/* 滚动条样式 */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.main-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-container {
    margin-left: 0;
  }
  
  .breadcrumb {
    font-size: 12px;
  }
  
  .username {
    font-size: 12px;
  }
  
  .logout-btn {
    padding: 4px 8px;
    font-size: 11px;
  }
}
</style>