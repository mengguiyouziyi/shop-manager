<template>
  <div class="order-cancelled">
    <div class="page-header">
      <h2>已取消订单</h2>
    </div>

    <el-card class="cancelled-card">
      <div class="cancelled-content">
        <p>已取消订单功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// 已取消订单页面
</script>

<style scoped>
.order-cancelled {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.cancelled-card {
  min-height: 400px;
}

.cancelled-content {
  text-align: center;
  padding: 100px 0;
  color: #909399;
}
</style>
