<template>
  <div class="simple-test">
    <h1>简单测试页面</h1>
    <p>如果您能看到这个页面，说明基本路由和组件渲染正常。</p>
    
    <div class="test-content">
      <h3>当前时间: {{ currentTime }}</h3>
      <p>Vue版本: {{ vueVersion }}</p>
      <p>页面路径: {{ currentPath }}</p>
    </div>
    
    <div class="test-buttons">
      <el-button type="primary" @click="showMessage">测试Element Plus</el-button>
      <el-button type="success" @click="testConsole">测试控制台</el-button>
      <el-button type="warning" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const currentTime = ref('')
const vueVersion = ref('3.x')
const currentPath = ref('')

onMounted(() => {
  currentTime.value = new Date().toLocaleString('zh-CN')
  currentPath.value = route.path
  console.log('SimpleTest页面已加载')
})

const showMessage = () => {
  ElMessage.success('Element Plus组件正常工作！')
}

const testConsole = () => {
  console.log('控制台测试成功')
  console.log('当前路由:', route.path)
  console.log('路由参数:', route.params)
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.simple-test {
  padding: 40px;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.test-content {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
}

.test-buttons {
  margin: 20px 0;
}

.test-buttons .el-button {
  margin: 0 10px;
}
</style>
