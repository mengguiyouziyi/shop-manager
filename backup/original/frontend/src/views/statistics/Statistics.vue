<template>
  <div class="statistics">
    <div class="page-header">
      <h2>统计报表</h2>
    </div>

    <div class="date-filter">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="loadStatistics"
      />
    </div>

    <div class="summary-cards">
      <el-card class="summary-card">
        <div class="card-content">
          <div class="card-icon sales">
            <el-icon><Money /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-title">总销售额</div>
            <div class="card-value">¥{{ statistics.totalSales || 0 }}</div>
            <div class="card-change positive">
              环比 {{ statistics.salesGrowth || 0 }}%
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="summary-card">
        <div class="card-content">
          <div class="card-icon orders">
            <el-icon><List /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-title">订单数量</div>
            <div class="card-value">{{ statistics.totalOrders || 0 }}</div>
            <div class="card-change positive">
              环比 {{ statistics.ordersGrowth || 0 }}%
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="summary-card">
        <div class="card-content">
          <div class="card-icon customers">
            <el-icon><User /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-title">客流量</div>
            <div class="card-value">{{ statistics.totalCustomers || 0 }}</div>
            <div class="card-change positive">
              环比 {{ statistics.customersGrowth || 0 }}%
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="summary-card">
        <div class="card-content">
          <div class="card-icon avg-order">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-title">客单价</div>
            <div class="card-value">¥{{ statistics.avgOrder || 0 }}</div>
            <div class="card-change negative">
              环比 -{{ statistics.avgOrderDecline || 0 }}%
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <div class="charts">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>销售趋势</span>
              </div>
            </template>
            <div class="chart-placeholder">
              <p>销售趋势图表</p>
              <p>显示指定时间范围内的销售额变化趋势</p>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>商品销售排行</span>
              </div>
            </template>
            <div class="chart-placeholder">
              <p>商品销售排行图表</p>
              <p>显示热销商品的销量排行</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="detail-tables">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card>
            <template #header>
              <span>销售明细</span>
            </template>
            <el-table :data="salesDetails" style="width: 100%">
              <el-table-column prop="date" label="日期" />
              <el-table-column prop="sales" label="销售额">
                <template #default="scope">
                  ¥{{ scope.row.sales }}
                </template>
              </el-table-column>
              <el-table-column prop="orders" label="订单数" />
              <el-table-column prop="customers" label="客数" />
              <el-table-column prop="avg_order" label="客单价">
                <template #default="scope">
                  ¥{{ scope.row.avg_order }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const dateRange = ref([])
const statistics = reactive({
  totalSales: 0,
  salesGrowth: 0,
  totalOrders: 0,
  ordersGrowth: 0,
  totalCustomers: 0,
  customersGrowth: 0,
  avgOrder: 0,
  avgOrderDecline: 0
})

const salesDetails = ref([])

onMounted(() => {
  // 设置默认日期范围（最近7天）
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 7)
  dateRange.value = [start, end]
  
  loadStatistics()
})

const loadStatistics = async () => {
  try {
    // 模拟API调用
    setTimeout(() => {
      Object.assign(statistics, {
        totalSales: 2847.50,
        salesGrowth: 12.5,
        totalOrders: 45,
        ordersGrowth: 8.3,
        totalCustomers: 38,
        customersGrowth: 15.2,
        avgOrder: 63.28,
        avgOrderDecline: 2.1
      })

      salesDetails.value = [
        { date: '2024-01-01', sales: 450.00, orders: 8, customers: 7, avg_order: 56.25 },
        { date: '2024-01-02', sales: 380.00, orders: 6, customers: 5, avg_order: 63.33 },
        { date: '2024-01-03', sales: 520.00, orders: 9, customers: 8, avg_order: 57.78 },
        { date: '2024-01-04', sales: 680.00, orders: 11, customers: 10, avg_order: 61.82 },
        { date: '2024-01-05', sales: 817.50, orders: 11, customers: 8, avg_order: 74.32 }
      ]
    }, 500)
  } catch (error) {
    ElMessage.error('加载统计数据失败')
  }
}
</script>

<style scoped>
.statistics {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.date-filter {
  margin-bottom: 20px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  color: white;
}

.card-icon.sales {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.orders {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.customers {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.avg-order {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-info {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.card-change {
  font-size: 12px;
}

.card-change.positive {
  color: #67c23a;
}

.card-change.negative {
  color: #f56c6c;
}

.charts {
  margin-bottom: 30px;
}

.chart-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chart-placeholder {
  text-align: center;
  padding: 60px 20px;
  color: #999;
  background: #f8f9fa;
  border-radius: 4px;
}

.chart-placeholder p {
  margin: 5px 0;
}

.detail-tables {
  margin-bottom: 30px;
}
</style>