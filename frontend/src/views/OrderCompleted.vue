<template>
  <div class="order-completed">
    <div class="page-header">
      <h2>已完成订单</h2>
    </div>

    <el-card class="completed-card">
      <div class="completed-content">
        <p>已完成订单功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// 已完成订单页面
</script>

<style scoped>
.order-completed {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.completed-card {
  min-height: 400px;
}

.completed-content {
  text-align: center;
  padding: 100px 0;
  color: #909399;
}
</style>
