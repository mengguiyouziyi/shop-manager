<template>
  <div class="promotions">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>促销活动管理</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            创建活动
          </el-button>
        </div>
      </template>

      <!-- 活动概览 -->
      <div class="promotion-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="overview-card active">
              <div class="overview-content">
                <div class="overview-icon">
                  <el-icon><Timer /></el-icon>
                </div>
                <div class="overview-info">
                  <div class="overview-number">{{ overview.active }}</div>
                  <div class="overview-label">进行中活动</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="overview-card upcoming">
              <div class="overview-content">
                <div class="overview-icon">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="overview-info">
                  <div class="overview-number">{{ overview.upcoming }}</div>
                  <div class="overview-label">即将开始</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="overview-card ended">
              <div class="overview-content">
                <div class="overview-icon">
                  <el-icon><Check /></el-icon>
                </div>
                <div class="overview-info">
                  <div class="overview-number">{{ overview.ended }}</div>
                  <div class="overview-label">已结束</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="overview-card total">
              <div class="overview-content">
                <div class="overview-icon">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="overview-info">
                  <div class="overview-number">¥{{ formatNumber(overview.totalRevenue) }}</div>
                  <div class="overview-label">活动总收入</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 搜索和筛选 -->
      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索活动名称"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.type" placeholder="活动类型" clearable>
              <el-option label="折扣活动" value="discount" />
              <el-option label="满减活动" value="full_reduction" />
              <el-option label="限时特价" value="flash_sale" />
              <el-option label="买赠活动" value="buy_gift" />
              <el-option label="积分活动" value="points" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.status" placeholder="活动状态" clearable>
              <el-option label="进行中" value="active" />
              <el-option label="即将开始" value="upcoming" />
              <el-option label="已结束" value="ended" />
              <el-option label="已暂停" value="paused" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 活动列表 -->
      <div class="promotion-list">
        <el-row :gutter="20">
          <el-col 
            v-for="promotion in promotionList" 
            :key="promotion.id" 
            :span="8"
            style="margin-bottom: 20px;"
          >
            <el-card class="promotion-card" :class="getPromotionClass(promotion.status)">
              <div class="promotion-header">
                <div class="promotion-type">
                  <el-tag :type="getTypeTagType(promotion.type)">
                    {{ getTypeLabel(promotion.type) }}
                  </el-tag>
                </div>
                <div class="promotion-status">
                  <el-tag :type="getStatusTagType(promotion.status)">
                    {{ getStatusLabel(promotion.status) }}
                  </el-tag>
                </div>
              </div>
              
              <div class="promotion-title">{{ promotion.name }}</div>
              <div class="promotion-desc">{{ promotion.description }}</div>
              
              <div class="promotion-info">
                <div class="info-item">
                  <span class="label">活动时间:</span>
                  <span class="value">{{ formatDateRange(promotion.start_time, promotion.end_time) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">参与商品:</span>
                  <span class="value">{{ promotion.product_count }}个</span>
                </div>
                <div class="info-item">
                  <span class="label">活动规则:</span>
                  <span class="value">{{ getRuleDescription(promotion) }}</span>
                </div>
              </div>
              
              <div class="promotion-stats">
                <div class="stat-item">
                  <div class="stat-number">{{ promotion.order_count }}</div>
                  <div class="stat-label">订单数</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">¥{{ formatNumber(promotion.revenue) }}</div>
                  <div class="stat-label">收入</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ promotion.customer_count }}</div>
                  <div class="stat-label">参与客户</div>
                </div>
              </div>
              
              <div class="promotion-actions">
                <el-button size="small" @click="handleView(promotion)">查看详情</el-button>
                <el-button size="small" type="primary" @click="handleEdit(promotion)">编辑</el-button>
                <el-button 
                  size="small" 
                  :type="promotion.status === 'active' ? 'warning' : 'success'"
                  @click="handleToggleStatus(promotion)"
                >
                  {{ promotion.status === 'active' ? '暂停' : '启用' }}
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(promotion)">删除</el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <div v-if="promotionList.length === 0" class="no-promotions">
          <el-icon><Gift /></el-icon>
          <p>暂无促销活动</p>
          <el-button type="primary" @click="showCreateDialog = true">创建第一个活动</el-button>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[12, 24, 48, 96]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 创建/编辑活动对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="isEdit ? '编辑活动' : '创建活动'"
      width="800px"
    >
      <el-form
        ref="promotionFormRef"
        :model="promotionForm"
        :rules="promotionRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动名称" prop="name">
              <el-input v-model="promotionForm.name" placeholder="请输入活动名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="活动类型" prop="type">
              <el-select v-model="promotionForm.type" placeholder="请选择活动类型" style="width: 100%">
                <el-option label="折扣活动" value="discount" />
                <el-option label="满减活动" value="full_reduction" />
                <el-option label="限时特价" value="flash_sale" />
                <el-option label="买赠活动" value="buy_gift" />
                <el-option label="积分活动" value="points" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_time">
              <el-date-picker
                v-model="promotionForm.start_time"
                type="datetime"
                placeholder="选择开始时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_time">
              <el-date-picker
                v-model="promotionForm.end_time"
                type="datetime"
                placeholder="选择结束时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="活动描述" prop="description">
          <el-input 
            v-model="promotionForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入活动描述"
          />
        </el-form-item>
        
        <!-- 活动规则配置 -->
        <el-divider content-position="left">
          <span class="section-title">🎯 活动规则</span>
        </el-divider>
        
        <div v-if="promotionForm.type === 'discount'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="折扣比例" prop="discount_rate">
                <el-input-number
                  v-model="promotionForm.discount_rate"
                  :min="0.1"
                  :max="9.9"
                  :precision="1"
                  :step="0.1"
                  style="width: 100%"
                  placeholder="8.5"
                >
                  <template #suffix>折</template>
                </el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="最低消费" prop="min_amount">
                <el-input-number
                  v-model="promotionForm.min_amount"
                  :min="0"
                  :precision="2"
                  :step="0.01"
                  style="width: 100%"
                  placeholder="0.00"
                >
                  <template #prefix>¥</template>
                </el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <div v-if="promotionForm.type === 'full_reduction'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="满减条件" prop="full_amount">
                <el-input-number
                  v-model="promotionForm.full_amount"
                  :min="0"
                  :precision="2"
                  :step="0.01"
                  style="width: 100%"
                  placeholder="100.00"
                >
                  <template #prefix>满¥</template>
                </el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="减免金额" prop="reduction_amount">
                <el-input-number
                  v-model="promotionForm.reduction_amount"
                  :min="0"
                  :precision="2"
                  :step="0.01"
                  style="width: 100%"
                  placeholder="20.00"
                >
                  <template #prefix>减¥</template>
                </el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <div v-if="promotionForm.type === 'flash_sale'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="特价价格" prop="flash_price">
                <el-input-number
                  v-model="promotionForm.flash_price"
                  :min="0"
                  :precision="2"
                  :step="0.01"
                  style="width: 100%"
                  placeholder="0.00"
                >
                  <template #prefix>¥</template>
                </el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="限购数量" prop="limit_quantity">
                <el-input-number
                  v-model="promotionForm.limit_quantity"
                  :min="1"
                  :precision="0"
                  style="width: 100%"
                  placeholder="1"
                >
                  <template #suffix>件</template>
                </el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <el-form-item label="参与商品" prop="product_ids">
          <el-select
            v-model="promotionForm.product_ids"
            multiple
            filterable
            placeholder="请选择参与活动的商品"
            style="width: 100%"
          >
            <el-option
              v-for="product in productList"
              :key="product.id"
              :label="product.name"
              :value="product.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="活动状态" prop="status">
          <el-radio-group v-model="promotionForm.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="paused">暂停</el-radio>
            <el-radio value="draft">草稿</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="saving">
            {{ saving ? '保存中...' : '保存' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { 
  Plus, Search, Refresh, Timer, Clock, Check, TrendCharts 
} from '@element-plus/icons-vue'

// 响应式数据
const showCreateDialog = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const promotionList = ref([])
const productList = ref([])

// 搜索表单
const searchForm = reactive({
  keyword: '',
  type: '',
  status: ''
})

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 12,
  total: 0
})

// 活动概览
const overview = reactive({
  active: 3,
  upcoming: 2,
  ended: 8,
  totalRevenue: 125680.50
})

// 表单引用
const promotionFormRef = ref<FormInstance>()

// 活动表单
const promotionForm = reactive({
  id: null,
  name: '',
  type: '',
  start_time: null,
  end_time: null,
  description: '',
  discount_rate: 8.5,
  min_amount: 0,
  full_amount: 100,
  reduction_amount: 20,
  flash_price: 0,
  limit_quantity: 1,
  product_ids: [],
  status: 'active'
})

// 表单验证规则
const promotionRules: FormRules = {
  name: [
    { required: true, message: '请输入活动名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择活动类型', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  product_ids: [
    { required: true, message: '请选择参与商品', trigger: 'change' }
  ]
}

// 生命周期
onMounted(() => {
  loadPromotions()
  loadProducts()
})

// 加载促销活动
const loadPromotions = async () => {
  try {
    // 模拟数据
    promotionList.value = [
      {
        id: 1,
        name: '双11全场8折',
        type: 'discount',
        status: 'active',
        description: '双11购物节，全场商品8折优惠',
        start_time: '2024-11-11 00:00:00',
        end_time: '2024-11-11 23:59:59',
        product_count: 156,
        order_count: 89,
        revenue: 45680.50,
        customer_count: 234
      },
      {
        id: 2,
        name: '满100减20',
        type: 'full_reduction',
        status: 'active',
        description: '满100元立减20元，多买多减',
        start_time: '2024-11-01 00:00:00',
        end_time: '2024-11-30 23:59:59',
        product_count: 89,
        order_count: 156,
        revenue: 67890.00,
        customer_count: 456
      }
    ]
    pagination.total = promotionList.value.length
  } catch (error) {
    console.error('加载促销活动失败:', error)
  }
}

// 加载商品列表
const loadProducts = async () => {
  try {
    // 模拟数据
    productList.value = [
      { id: 1, name: 'iPhone 15 Pro' },
      { id: 2, name: 'MacBook Air' },
      { id: 3, name: 'AirPods Pro' }
    ]
  } catch (error) {
    console.error('加载商品列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadPromotions()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    keyword: '',
    type: '',
    status: ''
  })
  pagination.current = 1
  loadPromotions()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.current = 1
  loadPromotions()
}

const handleCurrentChange = (page: number) => {
  pagination.current = page
  loadPromotions()
}

// 查看活动
const handleView = (promotion: any) => {
  ElMessage.info('查看活动详情功能开发中...')
}

// 编辑活动
const handleEdit = (promotion: any) => {
  isEdit.value = true
  Object.assign(promotionForm, promotion)
  showCreateDialog.value = true
}

// 切换状态
const handleToggleStatus = async (promotion: any) => {
  try {
    const action = promotion.status === 'active' ? '暂停' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}活动"${promotion.name}"吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用API
    promotion.status = promotion.status === 'active' ? 'paused' : 'active'
    ElMessage.success(`活动已${action}`)
    
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

// 删除活动
const handleDelete = async (promotion: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除活动"${promotion.name}"吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用API
    const index = promotionList.value.findIndex(item => item.id === promotion.id)
    if (index > -1) {
      promotionList.value.splice(index, 1)
      pagination.total--
    }
    ElMessage.success('活动删除成功')
    
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!promotionFormRef.value) return
  
  try {
    await promotionFormRef.value.validate()
    saving.value = true
    
    // 这里应该调用API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(isEdit.value ? '活动更新成功' : '活动创建成功')
    showCreateDialog.value = false
    
    // 重置表单
    if (!isEdit.value) {
      Object.assign(promotionForm, {
        id: null,
        name: '',
        type: '',
        start_time: null,
        end_time: null,
        description: '',
        discount_rate: 8.5,
        min_amount: 0,
        full_amount: 100,
        reduction_amount: 20,
        flash_price: 0,
        limit_quantity: 1,
        product_ids: [],
        status: 'active'
      })
    }
    
    loadPromotions()
    
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

// 工具函数
const formatNumber = (num: number): string => {
  if (!num) return '0.00'
  return num.toLocaleString('zh-CN', { minimumFractionDigits: 2 })
}

const formatDateRange = (start: string, end: string): string => {
  if (!start || !end) return ''
  const startDate = new Date(start).toLocaleDateString('zh-CN')
  const endDate = new Date(end).toLocaleDateString('zh-CN')
  return `${startDate} - ${endDate}`
}

const getPromotionClass = (status: string): string => {
  const classMap: Record<string, string> = {
    'active': 'active',
    'upcoming': 'upcoming',
    'ended': 'ended',
    'paused': 'paused'
  }
  return classMap[status] || ''
}

const getTypeTagType = (type: string): string => {
  const typeMap: Record<string, string> = {
    'discount': 'success',
    'full_reduction': 'warning',
    'flash_sale': 'danger',
    'buy_gift': 'info',
    'points': 'primary'
  }
  return typeMap[type] || 'info'
}

const getTypeLabel = (type: string): string => {
  const labelMap: Record<string, string> = {
    'discount': '折扣活动',
    'full_reduction': '满减活动',
    'flash_sale': '限时特价',
    'buy_gift': '买赠活动',
    'points': '积分活动'
  }
  return labelMap[type] || type
}

const getStatusTagType = (status: string): string => {
  const statusMap: Record<string, string> = {
    'active': 'success',
    'upcoming': 'warning',
    'ended': 'info',
    'paused': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const labelMap: Record<string, string> = {
    'active': '进行中',
    'upcoming': '即将开始',
    'ended': '已结束',
    'paused': '已暂停'
  }
  return labelMap[status] || status
}

const getRuleDescription = (promotion: any): string => {
  switch (promotion.type) {
    case 'discount':
      return `全场${promotion.discount_rate || 8}折`
    case 'full_reduction':
      return `满${promotion.full_amount || 100}减${promotion.reduction_amount || 20}`
    case 'flash_sale':
      return `限时特价¥${promotion.flash_price || 0}`
    case 'buy_gift':
      return '买一赠一'
    case 'points':
      return '双倍积分'
    default:
      return '暂无规则'
  }
}
</script>

<style scoped>
.promotions {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.promotion-overview {
  margin-bottom: 30px;
}

.overview-card {
  text-align: center;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.overview-card.active {
  border-left: 4px solid #67c23a;
}

.overview-card.upcoming {
  border-left: 4px solid #e6a23c;
}

.overview-card.ended {
  border-left: 4px solid #909399;
}

.overview-card.total {
  border-left: 4px solid #409eff;
}

.overview-content {
  display: flex;
  align-items: center;
  padding: 20px;
}

.overview-icon {
  font-size: 48px;
  margin-right: 20px;
  color: #409eff;
}

.overview-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.overview-label {
  font-size: 14px;
  color: #909399;
}

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.promotion-list {
  margin-bottom: 20px;
}

.promotion-card {
  height: 100%;
  transition: all 0.3s;
}

.promotion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.promotion-card.active {
  border-left: 4px solid #67c23a;
}

.promotion-card.upcoming {
  border-left: 4px solid #e6a23c;
}

.promotion-card.ended {
  border-left: 4px solid #909399;
}

.promotion-card.paused {
  border-left: 4px solid #f56c6c;
}

.promotion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.promotion-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.promotion-desc {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}

.promotion-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.info-item .label {
  color: #909399;
}

.info-item .value {
  color: #606266;
  font-weight: 500;
}

.promotion-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  padding: 15px 0;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.promotion-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.no-promotions {
  text-align: center;
  padding: 60px 0;
  color: #909399;
}

.no-promotions .el-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.no-promotions p {
  font-size: 16px;
  margin-bottom: 20px;
}

.pagination-section {
  margin-top: 20px;
  text-align: right;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
