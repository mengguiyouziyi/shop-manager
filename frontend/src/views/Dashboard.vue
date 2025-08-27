<template>
  <div class="dashboard">
    <h1>仪表盘</h1>
    <p>欢迎使用店铺管理系统</p>
    
    <div class="debug-info">
      <h3>调试信息</h3>
      <p>当前路由: {{ $route.path }}</p>
      <p>当前路由名称: {{ $route.name }}</p>
      <p>侧边栏应该显示菜单项</p>
    </div>
    
    <div class="quick-actions">
      <h3>快速操作</h3>
      <div class="action-buttons">
        <button @click="goToProducts">商品管理</button>
        <button @click="goToOrders">订单管理</button>
        <button @click="goToMembers">会员管理</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goToProducts = () => router.push('/products')
const goToOrders = () => router.push('/orders')
const goToMembers = () => router.push('/members')
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard h1 {
  color: #303133;
  margin-bottom: 20px;
}

.debug-info {
  margin: 20px 0;
  padding: 15px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 4px;
}

.debug-info h3 {
  color: #0369a1;
  margin-bottom: 10px;
}

.debug-info p {
  margin: 5px 0;
  color: #0c4a6e;
}

.quick-actions {
  margin-top: 30px;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 15px;
}

.action-buttons button {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.action-buttons button:hover {
  background: #337ecc;
}
</style>