<template>
  <div class="statistics">
    <h1>📈 数据统计</h1>
    <p>数据统计功能开发中...</p>
    
    <div class="actions">
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
.statistics {
  padding: 20px;
}

.statistics h1 {
  color: #303133;
  margin-bottom: 20px;
}

.actions {
  margin-top: 30px;
}

.actions button {
  padding: 10px 20px;
  background: #e6a23c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.actions button:hover {
  background: #cf9236;
}
</style>
