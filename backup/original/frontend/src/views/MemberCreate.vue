<template>
  <div class="member-create">
    <div class="page-header">
      <h2>创建会员</h2>
    </div>

    <el-card class="form-card">
      <MemberForm />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import MemberForm from '@/components/MemberForm.vue'
</script>

<style scoped>
.member-create {
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
  max-width: 800px;
  margin: 0 auto;
}
</style>
