<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="logo">🏪 Shop Manager</h1>
        <p class="subtitle">店铺管理系统</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="shop_id">
          <el-input
            v-model="loginForm.shop_id"
            placeholder="店铺ID"
            size="large"
            prefix-icon="Shop"
            type="number"
          />
        </el-form-item>
        
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            type="password"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p class="demo-info">
          <strong>演示账户:</strong><br>
          用户名: admin, 密码: password, 店铺ID: 1<br>
          用户名: user, 密码: password, 店铺ID: 1
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Shop, User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 响应式数据
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  shop_id: 1,
  username: '',
  password: ''
})

// 表单验证规则
const loginRules: FormRules = {
  shop_id: [
    { required: true, message: '请输入店铺ID', trigger: 'blur' },
    { type: 'number', min: 1, message: '店铺ID必须大于0', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在2到20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6到20个字符', trigger: 'blur' }
  ]
}

// 登录方法
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 表单验证
    await loginFormRef.value.validate()
    
    loading.value = true
    
    // 调用登录API
    await authStore.login(loginForm)
    
    ElMessage.success('登录成功！')
    
    // 跳转到仪表板
    router.push('/dashboard')
    
  } catch (error: any) {
    console.error('登录失败:', error)
    
    if (error.response?.status === 401) {
      ElMessage.error('用户名或密码错误')
    } else if (error.response?.status === 404) {
      ElMessage.error('店铺不存在')
    } else {
      ElMessage.error(error.message || '登录失败，请重试')
    }
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  // 如果已经登录，直接跳转到仪表板
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
  
  // 预填充演示账户信息
  loginForm.username = 'admin'
  loginForm.password = 'password'
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  font-size: 32px;
  margin: 0 0 10px 0;
  color: #409EFF;
}

.subtitle {
  color: #909399;
  margin: 0;
  font-size: 16px;
}

.login-form {
  margin-bottom: 20px;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.demo-info {
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.demo-info strong {
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
    margin: 20px;
  }
  
  .logo {
    font-size: 28px;
  }
  
  .subtitle {
    font-size: 14px;
  }
}
</style>
