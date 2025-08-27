<template>
  <div class="test-page">
    <h1>🧪 测试页面</h1>
    <p>如果您能看到这个页面，说明路由和布局都正常工作！</p>
    
    <el-card class="test-card">
      <h3>当前路由信息：</h3>
      <p><strong>路径：</strong>{{ route.path }}</p>
      <p><strong>名称：</strong>{{ route.name }}</p>
      <p><strong>参数：</strong>{{ route.params }}</p>
    </el-card>
    
    <el-card class="test-card">
      <h3>测试导航：</h3>
      <el-button @click="goToDashboard">前往仪表盘</el-button>
      <el-button @click="goToProducts">前往商品管理</el-button>
      <el-button @click="goToOrders">前往订单管理</el-button>
    </el-card>
    
    <el-card class="test-card">
      <h3>用户信息：</h3>
      <p><strong>认证状态：</strong>{{ authStore.isAuthenticated ? '已登录' : '未登录' }}</p>
      <p><strong>用户：</strong>{{ authStore.user?.name || '未知' }}</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const goToDashboard = () => router.push('/dashboard')
const goToProducts = () => router.push('/products')
const goToOrders = () => router.push('/orders')
</script>

<style scoped>
.test-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.test-card {
  margin-bottom: 20px;
}

.test-card h3 {
  margin-top: 0;
  color: #409eff;
}

.el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>
