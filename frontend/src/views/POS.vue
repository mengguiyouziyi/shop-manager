<template>
  <div class="pos">
    <h1>💰 POS收银</h1>
    <p>POS收银功能开发中...</p>
    
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
.pos {
  padding: 20px;
}

.pos h1 {
  color: #303133;
  margin-bottom: 20px;
}

.actions {
  margin-top: 30px;
}

.actions button {
  padding: 10px 20px;
  background: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.actions button:hover {
  background: #5daf34;
}
</style>
