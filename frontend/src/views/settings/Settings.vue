<template>
  <div class="settings">
    <div class="page-header">
      <h2>系统设置</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>店铺信息</span>
          </template>
          <el-form :model="shopInfo" label-width="100px">
            <el-form-item label="店铺名称">
              <el-input v-model="shopInfo.name" />
            </el-form-item>
            <el-form-item label="店铺地址">
              <el-input v-model="shopInfo.address" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="shopInfo.phone" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveShopInfo">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <span>系统配置</span>
          </template>
          <el-form :model="systemConfig" label-width="100px">
            <el-form-item label="货币符号">
              <el-input v-model="systemConfig.currency" />
            </el-form-item>
            <el-form-item label="时区">
              <el-select v-model="systemConfig.timezone">
                <el-option label="北京时间" value="Asia/Shanghai" />
                <el-option label="UTC时间" value="UTC" />
              </el-select>
            </el-form-item>
            <el-form-item label="语言">
              <el-select v-model="systemConfig.language">
                <el-option label="中文" value="zh-CN" />
                <el-option label="英文" value="en-US" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSystemConfig">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <span>数据管理</span>
          </template>
          <div class="data-management">
            <el-button type="primary" @click="backupData" :loading="backupLoading">
              备份数据
            </el-button>
            <el-button type="warning" @click="restoreData" :loading="restoreLoading">
              恢复数据
            </el-button>
            <el-button type="danger" @click="clearData">
              清空数据
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>操作日志</span>
          </template>
          <el-table :data="logs" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="user" label="操作用户" width="120" />
            <el-table-column prop="action" label="操作" />
            <el-table-column prop="ip" label="IP地址" width="140" />
            <el-table-column prop="result" label="结果" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.result === '成功' ? 'success' : 'danger'">
                  {{ scope.row.result }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const shopInfo = reactive({
  name: '示例店铺',
  address: '示例地址123号',
  phone: '13800138000'
})

const systemConfig = reactive({
  currency: '¥',
  timezone: 'Asia/Shanghai',
  language: 'zh-CN'
})

const backupLoading = ref(false)
const restoreLoading = ref(false)
const logs = ref([])

onMounted(() => {
  loadLogs()
})

const loadLogs = async () => {
  try {
    // 模拟API调用
    setTimeout(() => {
      logs.value = [
        { time: '2024-01-01 10:00:00', user: 'admin', action: '用户登录', ip: '192.168.1.100', result: '成功' },
        { time: '2024-01-01 10:05:00', user: 'admin', action: '修改商品', ip: '192.168.1.100', result: '成功' },
        { time: '2024-01-01 10:10:00', user: 'staff', action: '创建订单', ip: '192.168.1.101', result: '成功' },
        { time: '2024-01-01 10:15:00', user: 'admin', action: '备份数据', ip: '192.168.1.100', result: '成功' }
      ]
    }, 500)
  } catch (error) {
    ElMessage.error('加载日志失败')
  }
}

const saveShopInfo = () => {
  ElMessage.success('店铺信息保存成功')
}

const saveSystemConfig = () => {
  ElMessage.success('系统配置保存成功')
}

const backupData = async () => {
  backupLoading.value = true
  try {
    // 模拟备份操作
    setTimeout(() => {
      ElMessage.success('数据备份成功')
      backupLoading.value = false
    }, 2000)
  } catch (error) {
    ElMessage.error('数据备份失败')
    backupLoading.value = false
  }
}

const restoreData = async () => {
  restoreLoading.value = true
  try {
    // 模拟恢复操作
    setTimeout(() => {
      ElMessage.success('数据恢复成功')
      restoreLoading.value = false
    }, 2000)
  } catch (error) {
    ElMessage.error('数据恢复失败')
    restoreLoading.value = false
  }
}

const clearData = () => {
  ElMessage.warning('清空数据功能开发中')
}
</script>

<style scoped>
.settings {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.data-management {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.data-management .el-button {
  width: 100%;
}
</style>