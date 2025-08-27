<template>
  <div class="order-create">
    <div class="page-header">
      <h2>创建订单</h2>
    </div>

    <el-card class="form-card">
      <OrderForm />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import OrderForm from '@/components/OrderForm.vue'
</script>

<style scoped>
.order-create {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.form-card {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
