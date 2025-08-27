<template>
  <div class="shop-create">
    <div class="page-header">
      <h2>创建店铺</h2>
      <el-button @click="$router.go(-1)" type="default">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
    </div>

    <el-card class="form-card">
      <ShopForm />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
import ShopForm from '@/components/ShopForm.vue'
</script>

<style scoped>
.shop-create {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
}
</style>
