<template>
  <div class="order-detail">
    <div class="page-header">
      <h2>订单详情</h2>
      <el-button @click="goBack">返回</el-button>
    </div>

    <div v-if="order" class="order-content">
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="order-info">
            <template #header>
              <span>订单信息</span>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="订单号">{{ order.order_no }}</el-descriptions-item>
              <el-descriptions-item label="订单状态">
                <el-tag :type="getOrderStatusType(order.status)">
                  {{ getOrderStatusText(order.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="支付状态">
                <el-tag :type="getPaymentStatusType(order.payment_status)">
                  {{ getPaymentStatusText(order.payment_status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="支付方式">{{ order.payment_method }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatDate(order.created_at) }}</el-descriptions-item>
              <el-descriptions-item label="会员">{{ order.member?.name || '非会员' }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <el-card class="order-items" style="margin-top: 20px">
            <template #header>
              <span>商品清单</span>
            </template>
            <el-table :data="order.items" style="width: 100%">
              <el-table-column prop="product.name" label="商品名称" />
              <el-table-column prop="price" label="单价" width="120">
                <template #default="scope">
                  ¥{{ scope.row.price }}
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="100" />
              <el-table-column prop="total_price" label="小计" width="120">
                <template #default="scope">
                  ¥{{ scope.row.total_price }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="order-summary">
            <template #header>
              <span>费用明细</span>
            </template>
            <div class="summary-item">
              <span>商品总额:</span>
              <span>¥{{ order.total_amount + (order.discount_amount || 0) }}</span>
            </div>
            <div class="summary-item">
              <span>优惠金额:</span>
              <span>-¥{{ order.discount_amount || 0 }}</span>
            </div>
            <div class="summary-item total">
              <span>实付金额:</span>
              <span class="total-amount">¥{{ order.total_amount }}</span>
            </div>
          </el-card>

          <el-card class="order-actions" style="margin-top: 20px">
            <template #header>
              <span>操作</span>
            </template>
            <el-button type="primary" @click="printOrder">打印小票</el-button>
            <el-button @click="exportOrder">导出订单</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()

const order = ref(null)

onMounted(() => {
  loadOrder()
})

const loadOrder = async () => {
  try {
    const orderId = route.params.id
    // 模拟API调用
    setTimeout(() => {
      order.value = {
        id: orderId,
        order_no: 'ORD202401010001',
        total_amount: 28.50,
        discount_amount: 2.00,
        payment_method: '现金',
        payment_status: 1,
        status: 2,
        created_at: '2024-01-01 10:00:00',
        member: { name: '张三' },
        items: [
          {
            product: { name: '方便面' },
            price: 5.50,
            quantity: 2,
            total_price: 11.00
          },
          {
            product: { name: '可乐' },
            price: 3.00,
            quantity: 3,
            total_price: 9.00
          },
          {
            product: { name: '面包' },
            price: 8.50,
            quantity: 1,
            total_price: 8.50
          }
        ]
      }
    }, 500)
  } catch (error) {
    ElMessage.error('加载订单详情失败')
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
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

const goBack = () => {
  router.push('/orders')
}

const printOrder = () => {
  ElMessage.info('打印功能开发中')
}

const exportOrder = () => {
  ElMessage.info('导出功能开发中')
}
</script>

<style scoped>
.order-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-content {
  min-height: 400px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.summary-item.total {
  font-weight: bold;
  font-size: 16px;
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.total-amount {
  color: #e74c3c;
}

.order-actions .el-button {
  width: 100%;
  margin-bottom: 10px;
}
</style>