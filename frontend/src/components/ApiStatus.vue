<template>
  <div class="api-status">
    <el-tooltip
      :content="statusText"
      placement="bottom"
      :show-after="500"
    >
      <div class="status-indicator" :class="statusClass">
        <el-icon :size="16">
          <component :is="statusIcon" />
        </el-icon>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </el-tooltip>
    
    <el-button
      v-if="!connected"
      size="small"
      type="primary"
      @click="checkConnection"
      :loading="checking"
    >
      重试连接
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Connection, Warning, Check } from '@element-plus/icons-vue'

// Props
interface Props {
  showButton?: boolean
  autoCheck?: boolean
  checkInterval?: number
}

const props = withDefaults(defineProps<Props>(), {
  showButton: true,
  autoCheck: true,
  checkInterval: 30000 // 30秒检查一次
})

// Emits
const emit = defineEmits<{
  statusChange: [connected: boolean]
}>()

// 响应式数据
const connected = ref(false)
const checking = ref(false)
const lastCheck = ref<Date | null>(null)

// 计算属性
const statusClass = computed(() => ({
  'status-connected': connected.value,
  'status-disconnected': !connected.value
}))

const statusText = computed(() => {
  if (checking.value) return '检查中...'
  return connected.value ? '已连接' : '未连接'
})

const statusIcon = computed(() => {
  if (checking.value) return Connection
  return connected.value ? Check : Warning
})

// 方法
const checkConnection = async () => {
  if (checking.value) return
  
  checking.value = true
  
  try {
    const apiBaseUrl = 'http://localhost:8000'
    
    const response = await fetch(`${apiBaseUrl}/health`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const wasConnected = connected.value
    connected.value = response.ok
    
    if (wasConnected !== connected.value) {
      emit('statusChange', connected.value)
      
      if (connected.value) {
        ElMessage.success('后端服务连接成功')
      } else {
        ElMessage.warning('后端服务连接失败')
      }
    }
    
    lastCheck.value = new Date()
  } catch (error) {
    const wasConnected = connected.value
    connected.value = false
    
    if (wasConnected !== connected.value) {
      emit('statusChange', connected.value)
      ElMessage.error('后端服务连接失败')
    }
    
    lastCheck.value = new Date()
  } finally {
    checking.value = false
  }
}

// 自动检查连接状态
let checkTimer: NodeJS.Timeout | null = null

const startAutoCheck = () => {
  if (props.autoCheck) {
    checkTimer = setInterval(checkConnection, props.checkInterval)
  }
}

const stopAutoCheck = () => {
  if (checkTimer) {
    clearInterval(checkTimer)
    checkTimer = null
  }
}

// 生命周期
onMounted(() => {
  checkConnection()
  startAutoCheck()
})

onUnmounted(() => {
  stopAutoCheck()
})

// 暴露方法给父组件
defineExpose({
  checkConnection,
  connected: computed(() => connected.value)
})
</script>

<style scoped>
.api-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-connected {
  background: #f0f9ff;
  color: #0369a1;
}

.status-disconnected {
  background: #fef2f2;
  color: #dc2626;
}

.status-text {
  font-size: 11px;
}

.el-button {
  height: 24px;
  padding: 0 8px;
  font-size: 11px;
}
</style>
