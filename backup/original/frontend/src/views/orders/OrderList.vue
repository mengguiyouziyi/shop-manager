<template>
  <div class="order-list">
    <div class="page-header">
      <h2>订单管理</h2>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索订单号"
        style="width: 200px"
        @input="handleSearch"
      />
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleSearch"
      />
      <el-select v-model="selectedStatus" placeholder="订单状态" @change="handleSearch">
        <el-option label="全部状态" value="" />
        <el-option label="待支付" value="0" />
        <el-option label="已支付" value="1" />
        <el-option label="已完成" value="2" />
        <el-option label="已取消" value="3" />
      </el-select>
    </div>

    <el-table :data="orders" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="order_no" label="订单号" width="150" />
      <el-table-column prop="member.name" label="会员" width="100" />
      <el-table-column prop="total_amount" label="总金额" width="120">
        <template #default="scope">
          ¥{{ scope.row.total_amount }}
        </template>
      </el-table-column>
      <el-table-column prop="discount_amount" label="优惠金额" width="120">
        <template #default="scope">
          ¥{{ scope.row.discount_amount || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="payment_method" label="支付方式" width="100" />
      <el-table-column prop="payment_status" label="支付状态" width="100">
        <template #default="scope">
          <el-tag :type="getPaymentStatusType(scope.row.payment_status)">
            {{ getPaymentStatusText(scope.row.payment_status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="订单状态" width="100">
        <template #default="scope">
          <el-tag :type="getOrderStatusType(scope.row.status)">
            {{ getOrderStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="viewOrder(scope.row)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>

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
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const searchKeyword = ref('')
const dateRange = ref([])
const selectedStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const orders = ref([])

onMounted(() => {
  loadOrders()
})

const loadOrders = async () => {
  loading.value = true
  try {
    // 模拟API调用
    setTimeout(() => {
      orders.value = [
        {
          id: 1,
          order_no: 'ORD202401010001',
          member: { name: '张三' },
          total_amount: 28.50,
          discount_amount: 2.00,
          payment_method: '现金',
          payment_status: 1,
          status: 2,
          created_at: '2024-01-01 10:00:00'
        },
        {
          id: 2,
          order_no: 'ORD202401010002',
          member: { name: '李四' },
          total_amount: 15.00,
          discount_amount: 0,
          payment_method: '微信',
          payment_status: 1,
          status: 2,
          created_at: '2024-01-01 11:00:00'
        },
        {
          id: 3,
          order_no: 'ORD202401010003',
          member: null,
          total_amount: 8.00,
          discount_amount: 0,
          payment_method: '支付宝',
          payment_status: 0,
          status: 1,
          created_at: '2024-01-01 12:00:00'
        }
      ]
      total.value = orders.value.length
      loading.value = false
    }, 500)
  } catch (error) {
    console.error('加载订单失败:', error)
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const getPaymentStatusType = (status: number) => {
  const types = {
    0: 'warning',
    1: 'success'
  }
  return types[status] || 'info'
}

const getPaymentStatusText = (status: number) => {
  const texts = {
    0: '待支付',
    1: '已支付'
  }
  return texts[status] || '未知'
}

const getOrderStatusType = (status: number) => {
  const types = {
    1: 'warning',
    2: 'success',
    3: 'danger'
  }
  return types[status] || 'info'
}

const getOrderStatusText = (status: number) => {
  const texts = {
    1: '进行中',
    2: '已完成',
    3: '已取消'
  }
  return texts[status] || '未知'
}

const handleSearch = () => {
  currentPage.value = 1
  loadOrders()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadOrders()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadOrders()
}

const viewOrder = (order: any) => {
  router.push(`/orders/${order.id}`)
}
</script>

<style scoped>
.order-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  text-align: right;
}
</style>