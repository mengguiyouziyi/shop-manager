<template>
  <div class="order-management-page">
    <div class="page-header">
      <h2>订单管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新建订单
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="hover">
      <el-form :model="searchForm" inline>
        <el-form-item label="订单号">
          <el-input
            v-model="searchForm.order_no"
            placeholder="输入订单号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="待支付" :value="1" />
            <el-option label="已支付" :value="2" />
            <el-option label="已发货" :value="3" />
            <el-option label="已完成" :value="4" />
            <el-option label="已取消" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select
            v-model="searchForm.payment_status"
            placeholder="选择支付状态"
            clearable
            style="width: 120px"
          >
            <el-option label="待支付" :value="1" />
            <el-option label="已支付" :value="2" />
            <el-option label="已退款" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 订单列表 -->
    <el-card class="table-card" shadow="hover">
      <div class="table-toolbar">
        <el-button
          type="danger"
          :disabled="selectedOrders.length === 0"
          @click="handleBatchDelete"
        >
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>

      <el-table
        :data="orders"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="order_no" label="订单号" width="180" />
        <el-table-column prop="total_amount" label="订单金额" width="120">
          <template #default="{ row }">
            ¥{{ row.total_amount.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="支付方式" width="100" />
        <el-table-column prop="status" label="订单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_status" label="支付状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getPaymentStatusType(row.payment_status)">
              {{ getPaymentStatusText(row.payment_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewOrder(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editOrder(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteOrder(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑订单对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="isEdit ? '编辑订单' : '新建订单'"
      width="800px"
    >
      <el-form :model="orderForm" :rules="orderRules" ref="orderFormRef" label-width="100px">
        <el-form-item label="会员" prop="member_id">
          <el-select
            v-model="orderForm.member_id"
            placeholder="选择会员"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="member in members"
              :key="member.id"
              :label="member.name"
              :value="member.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method">
          <el-select
            v-model="orderForm.payment_method"
            placeholder="选择支付方式"
            style="width: 100%"
          >
            <el-option label="现金" value="cash" />
            <el-option label="微信支付" value="wechat" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="银行卡" value="card" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品" prop="items">
          <div v-for="(item, index) in orderForm.items" :key="index" class="order-item">
            <el-row :gutter="10">
              <el-col :span="8">
                <el-select
                  v-model="item.product_id"
                  placeholder="选择商品"
                  @change="updateItemPrice(index)"
                >
                  <el-option
                    v-for="product in products"
                    :key="product.id"
                    :label="product.name"
                    :value="product.id"
                  />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-input-number
                  v-model="item.quantity"
                  :min="1"
                  placeholder="数量"
                  @change="updateItemPrice(index)"
                />
              </el-col>
              <el-col :span="4">
                <el-input-number
                  v-model="item.price"
                  :min="0"
                  :precision="2"
                  placeholder="单价"
                  @change="updateItemPrice(index)"
                />
              </el-col>
              <el-col :span="4">
                <el-input-number
                  v-model="item.total_price"
                  :min="0"
                  :precision="2"
                  placeholder="小计"
                  disabled
                />
              </el-col>
              <el-col :span="4">
                <el-button @click="removeOrderItem(index)" type="danger" size="small">
                  删除
                </el-button>
              </el-col>
            </el-row>
          </div>
          <el-button @click="addOrderItem" type="primary" size="small">
            <el-icon><Plus /></el-icon>
            添加商品
          </el-button>
        </el-form-item>
        <el-form-item label="折扣金额" prop="discount_amount">
          <el-input-number
            v-model="orderForm.discount_amount"
            :min="0"
            :precision="2"
            placeholder="折扣金额"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="订单总额">
          <el-input
            :value="`¥${orderForm.total_amount.toLocaleString()}`"
            disabled
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, Delete, Download } from '@element-plus/icons-vue'
import { ordersApi } from '@/api/orders'
import { productsApi } from '@/api/products'
import { membersApi } from '@/api/members'
import type { Order, OrderCreate, OrderUpdate } from '@/api/orders'
import type { Product } from '@/api/products'
import type { Member } from '@/api/members'

// 响应式数据
const loading = ref(false)
const orders = ref<Order[]>([])
const products = ref<Product[]>([])
const members = ref<Member[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const showAddDialog = ref(false)
const isEdit = ref(false)
const editingOrder = ref<Order | null>(null)
const selectedOrders = ref<Order[]>([])
const orderFormRef = ref()

// 搜索表单
const searchForm = reactive({
  order_no: '',
  status: undefined as number | undefined,
  payment_status: undefined as number | undefined
})

// 订单表单
const orderForm = reactive({
  shop_id: 1,
  member_id: undefined as number | undefined,
  payment_method: 'cash',
  items: [
    { product_id: undefined as number | undefined, quantity: 1, price: 0, total_price: 0 }
  ],
  discount_amount: 0,
  total_amount: 0
})

// 表单验证规则
const orderRules = {
  member_id: [{ required: true, message: '请选择会员', trigger: 'change' }],
  payment_method: [{ required: true, message: '请选择支付方式', trigger: 'change' }],
  items: [{ required: true, message: '请添加商品', trigger: 'change' }]
}

// 计算属性
const getStatusType = (status: number) => {
  const statusMap: Record<number, string> = {
    1: 'warning',
    2: 'success',
    3: 'primary',
    4: 'success',
    5: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: number) => {
  const statusMap: Record<number, string> = {
    1: '待支付',
    2: '已支付',
    3: '已发货',
    4: '已完成',
    5: '已取消'
  }
  return statusMap[status] || '未知'
}

const getPaymentStatusType = (status: number) => {
  const statusMap: Record<number, string> = {
    1: 'warning',
    2: 'success',
    3: 'danger'
  }
  return statusMap[status] || 'info'
}

const getPaymentStatusText = (status: number) => {
  const statusMap: Record<number, string> = {
    1: '待支付',
    2: '已支付',
    3: '已退款'
  }
  return statusMap[status] || '未知'
}

// 方法
const loadOrders = async () => {
  loading.value = true
  try {
    const response = await ordersApi.getOrders({
      page: currentPage.value,
      limit: pageSize.value,
      ...searchForm
    })
    orders.value = response
    total.value = response.length
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载订单失败')
  } finally {
    loading.value = false
  }
}

const loadProducts = async () => {
  try {
    const response = await productsApi.getProducts()
    products.value = response
  } catch (error) {
    console.error('加载商品失败:', error)
  }
}

const loadMembers = async () => {
  try {
    const response = await membersApi.getMembers()
    members.value = response
  } catch (error) {
    console.error('加载会员失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadOrders()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    order_no: '',
    status: undefined,
    payment_status: undefined
  })
  handleSearch()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadOrders()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadOrders()
}

const handleSelectionChange = (selection: Order[]) => {
  selectedOrders.value = selection
}

const viewOrder = (order: Order) => {
  console.log('查看订单:', order)
}

const editOrder = (order: Order) => {
  isEdit.value = true
  editingOrder.value = order
  Object.assign(orderForm, {
    shop_id: order.shop_id,
    member_id: order.member_id,
    payment_method: order.payment_method,
    items: order.items || [],
    discount_amount: order.discount_amount,
    total_amount: order.total_amount
  })
  showAddDialog.value = true
}

const deleteOrder = async (order: Order) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除订单 ${order.order_no} 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await ordersApi.deleteOrder(order.id)
    ElMessage.success('订单删除成功')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除订单失败:', error)
      ElMessage.error('删除订单失败')
    }
  }
}

const handleBatchDelete = async () => {
  if (selectedOrders.value.length === 0) {
    ElMessage.warning('请选择要删除的订单')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedOrders.value.length} 个订单吗？`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedOrders.value.map(o => o.id)
    for (const id of ids) {
      await ordersApi.deleteOrder(id)
    }
    
    ElMessage.success('批量删除成功')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

const addOrderItem = () => {
  orderForm.items.push({
    product_id: undefined,
    quantity: 1,
    price: 0,
    total_price: 0
  })
}

const removeOrderItem = (index: number) => {
  if (orderForm.items.length > 1) {
    orderForm.items.splice(index, 1)
    calculateTotal()
  }
}

const updateItemPrice = (index: number) => {
  const item = orderForm.items[index]
  if (item.product_id && item.quantity && item.price) {
    item.total_price = item.quantity * item.price
    calculateTotal()
  }
}

const calculateTotal = () => {
  const itemsTotal = orderForm.items.reduce((sum, item) => sum + (item.total_price || 0), 0)
  orderForm.total_amount = itemsTotal - orderForm.discount_amount
}

const resetForm = () => {
  editingOrder.value = null
  Object.assign(orderForm, {
    shop_id: 1,
    member_id: undefined,
    payment_method: 'cash',
    items: [{ product_id: undefined, quantity: 1, price: 0, total_price: 0 }],
    discount_amount: 0,
    total_amount: 0
  })
}

const handleSubmit = async () => {
  try {
    if (isEdit.value && editingOrder.value) {
      await ordersApi.updateOrder(editingOrder.value.id, orderForm as OrderUpdate)
      ElMessage.success('订单更新成功')
    } else {
      await ordersApi.createOrder(orderForm as OrderCreate)
      ElMessage.success('订单创建成功')
    }
    
    showAddDialog.value = false
    loadOrders()
    resetForm()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请重试')
  }
}

const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 生命周期
onMounted(() => {
  loadOrders()
  loadProducts()
  loadMembers()
})
</script>

<style scoped>
.order-management-page {
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

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.table-toolbar {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.order-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
