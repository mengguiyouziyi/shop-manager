<template>
  <div class="member-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑会员' : '添加会员' }}</h2>
      <el-button @click="goBack">返回</el-button>
    </div>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="member-form-content"
    >
      <el-form-item label="会员姓名" prop="name">
        <el-input v-model="formData.name" placeholder="请输入会员姓名" />
      </el-form-item>

      <el-form-item label="手机号码" prop="phone">
        <el-input v-model="formData.phone" placeholder="请输入手机号码" />
      </el-form-item>

      <el-form-item label="会员等级" prop="level">
        <el-select v-model="formData.level" placeholder="请选择会员等级">
          <el-option label="普通会员" value="普通会员" />
          <el-option label="VIP会员" value="VIP会员" />
          <el-option label="钻石会员" value="钻石会员" />
        </el-select>
      </el-form-item>

      <el-form-item label="积分" prop="points">
        <el-input-number
          v-model="formData.points"
          :min="0"
          :step="1"
        />
      </el-form-item>

      <el-form-item label="余额" prop="balance">
        <el-input-number
          v-model="formData.balance"
          :precision="2"
          :step="0.1"
          :min="0"
        />
      </el-form-item>

      <el-form-item label="生日" prop="birthday">
        <el-date-picker
          v-model="formData.birthday"
          type="date"
          placeholder="选择生日"
        />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="formData.status">
          <el-radio :label="1">正常</el-radio>
          <el-radio :label="0">停用</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input
          v-model="formData.remark"
          type="textarea"
          :rows="4"
          placeholder="请输入备注信息"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const formRef = ref()
const loading = ref(false)

const isEdit = computed(() => !!route.params.id)

const formData = reactive({
  name: '',
  phone: '',
  level: '普通会员',
  points: 0,
  balance: 0,
  birthday: '',
  status: 1,
  remark: ''
})

const rules = {
  name: [
    { required: true, message: '请输入会员姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

onMounted(() => {
  if (isEdit.value) {
    loadMember()
  }
})

const loadMember = async () => {
  try {
    const memberId = route.params.id
    // 模拟API调用
    setTimeout(() => {
      const memberData = {
        id: memberId,
        name: '张三',
        phone: '13900139000',
        level: '普通会员',
        points: 100,
        balance: 50.00,
        birthday: '1990-01-01',
        status: 1,
        remark: '优质客户'
      }
      
      Object.assign(formData, memberData)
    }, 500)
  } catch (error) {
    ElMessage.error('加载会员信息失败')
  }
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 模拟API调用
    setTimeout(() => {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      router.push('/members')
    }, 1000)
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

const goBack = () => {
  router.push('/members')
}
</script>

<style scoped>
.member-form {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.member-form-content {
  max-width: 600px;
  margin: 0 auto;
}
</style>