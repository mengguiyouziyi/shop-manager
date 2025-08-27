<template>
  <div class="home-page">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h1>🎉 欢迎使用{{ appStore.appName }}</h1>
        </div>
      </template>
      <p>系统已成功启动，所有基础功能正常！</p>
      <p><strong>版本:</strong> {{ appStore.version }} | <strong>最后更新:</strong> {{ appStore.lastUpdate }}</p>
    </el-card>
    
    <el-row :gutter="20" class="status-grid">
      <el-col :span="8">
        <el-card class="status-card">
          <template #header>
            <div class="card-header">
              <span>✅ 前端状态</span>
            </div>
          </template>
          <p>Vue 3.x + Vite 正常运行</p>
          <p>路由系统已启用</p>
          <p>Element Plus 已加载</p>
          <p>Pinia 状态管理已启用</p>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="status-card">
          <template #header>
            <div class="card-header">
              <span>🕒 系统时间</span>
            </div>
          </template>
          <p>{{ currentTime }}</p>
          <p>页面加载时间: {{ loadTime }}</p>
          <el-button size="small" @click="updateTime">更新时间</el-button>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="status-card">
          <template #header>
            <div class="card-header">
              <span>🔧 功能测试</span>
            </div>
          </template>
          <el-button type="primary" @click="testFunction">测试功能</el-button>
          <el-button type="success" @click="testStore" style="margin-left: 10px">测试Store</el-button>
          <el-alert
            v-if="testResult"
            :title="testResult"
            type="success"
            :closable="false"
            show-icon
            style="margin-top: 15px"
          />
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="quick-actions">
      <template #header>
        <div class="card-header">
          <span>快速操作</span>
        </div>
      </template>
      <div class="action-buttons">
        <el-button type="primary" @click="$router.push('/simple')">
          简单测试页面
        </el-button>
        <el-button type="success" @click="$router.push('/dashboard')">
          仪表板
        </el-button>
        <el-button type="warning" @click="refreshPage">
          刷新页面
        </el-button>
        <el-button type="info" @click="showAppInfo">
          应用信息
        </el-button>
      </div>
    </el-card>

    <!-- 通知区域 -->
    <el-card v-if="appStore.hasNotifications" class="notifications">
      <template #header>
        <div class="card-header">
          <span>📢 系统通知</span>
          <el-button size="small" @click="appStore.clearNotifications">清空</el-button>
        </div>
      </template>
      <div v-for="(notification, index) in appStore.notifications" :key="index" class="notification-item">
        <el-tag type="info" closable @close="appStore.removeNotification(notification)">
          {{ notification }}
        </el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const currentTime = ref('')
const loadTime = ref('')
const testResult = ref('')

onMounted(() => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN')
  loadTime.value = now.toLocaleTimeString('zh-CN')
  console.log('首页已加载')
  
  // 添加欢迎通知
  appStore.addNotification('欢迎使用店铺管理系统！')
})

const testFunction = () => {
  testResult.value = `功能测试成功 - ${new Date().toLocaleTimeString('zh-CN')}`
  ElMessage.success('功能测试成功！')
  appStore.addNotification('功能测试完成')
  setTimeout(() => {
    testResult.value = ''
  }, 3000)
}

const testStore = () => {
  appStore.updateAppInfo()
  appStore.addNotification('状态管理测试成功！')
  ElMessage.success('Store测试成功！')
}

const updateTime = () => {
  currentTime.value = new Date().toLocaleString('zh-CN')
  appStore.addNotification('时间已更新')
}

const refreshPage = () => {
  ElMessage.info('正在刷新页面...')
  appStore.addNotification('页面即将刷新')
  setTimeout(() => {
    window.location.reload()
  }, 1000)
}

const showAppInfo = () => {
  ElMessage.info(`应用名称: ${appStore.appName}, 版本: ${appStore.version}`)
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 30px;
}

.card-header {
  text-align: center;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h1 {
  color: #333;
  margin: 0;
  font-size: 1.8em;
}

.status-grid {
  margin-bottom: 30px;
}

.status-card {
  height: 100%;
}

.status-card p {
  color: #666;
  margin: 8px 0;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.notifications {
  margin-top: 20px;
}

.notification-item {
  margin: 8px 0;
}

.el-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-card :deep(.el-card__header) {
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}
</style>
