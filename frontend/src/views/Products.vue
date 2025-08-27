<template>
  <div class="products">
    <h1>商品管理</h1>
    <p>这是商品管理页面</p>
    
    <div class="test-content">
      <h3>测试内容</h3>
      <p>如果您看到这个页面，说明路由和组件都正常工作。</p>
      <button @click="goBack">返回仪表盘</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => router.push('/dashboard')
</script>

<style scoped>
.products {
  padding: 20px;
}

.products h1 {
  color: #303133;
  margin-bottom: 20px;
}

.test-content {
  margin-top: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.test-content button {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.test-content button:hover {
  background: #337ecc;
}
</style>

