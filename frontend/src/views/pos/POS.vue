<template>
  <div class="pos-container">
    <div class="pos-header">
      <h2>收银台</h2>
      <div class="pos-info">
        <span>当前时间: {{ currentTime }}</span>
        <span>操作员: {{ user?.name }}</span>
      </div>
    </div>

    <div class="pos-content">
      <div class="product-section">
        <div class="search-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="扫描条码或输入商品名称"
            size="large"
            @keyup.enter="searchProduct"
          >
            <template #append>
              <el-button @click="searchProduct">搜索</el-button>
            </template>
          </el-input>
        </div>

        <div class="product-grid">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-card"
            @click="addToCart(product)"
          >
            <div class="product-name">{{ product.name }}</div>
            <div class="product-price">¥{{ product.price }}</div>
            <div class="product-stock">库存: {{ product.stock }}</div>
          </div>
        </div>
      </div>

      <div class="order-section">
        <div class="order-header">
          <h3>当前订单</h3>
          <el-button type="danger" size="small" @click="clearOrder">清空</el-button>
        </div>

        <div class="order-items">
          <div v-if="cartItems.length === 0" class="empty-cart">
            购物车为空
          </div>
          <div v-else>
            <div v-for="(item, index) in cartItems" :key="index" class="order-item">
              <div class="item-info">
                <div class="item-name">{{ item.name }}</div>
                <div class="item-price">¥{{ item.price }}</div>
              </div>
              <div class="item-actions">
                <el-input-number
                  v-model="item.quantity"
                  :min="1"
                  :max="item.stock"
                  size="small"
                  @change="updateItemTotal(index)"
                />
                <div class="item-total">¥{{ item.total }}</div>
                <el-button type="danger" size="small" @click="removeFromCart(index)">
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <div class="order-summary">
          <div class="summary-item">
            <span>商品总数:</span>
            <span>{{ totalQuantity }}</span>
          </div>
          <div class="summary-item">
            <span>总金额:</span>
            <span class="total-amount">¥{{ totalAmount }}</span>
          </div>
        </div>

        <div class="payment-section">
          <el-button type="primary" size="large" @click="checkout" :disabled="cartItems.length === 0">
            结算 (¥{{ totalAmount }})
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const authStore = useAuthStore()
const user = authStore.user

const searchKeyword = ref('')
const products = ref([])
const cartItems = ref([])
const currentTime = ref(dayjs().format('YYYY-MM-DD HH:mm:ss'))

const totalQuantity = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

const totalAmount = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.total, 0)
})

onMounted(() => {
  loadProducts()
  setInterval(() => {
    currentTime.value = dayjs().format('YYYY-MM-DD HH:mm:ss')
  }, 1000)
})

const loadProducts = async () => {
  try {
    const response = await fetch('/api/products', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    const result = await response.json()
    
    if (result.success) {
      products.value = result.data.products
    } else {
      ElMessage.error('加载商品失败')
    }
  } catch (error) {
    console.error('Load products error:', error)
    ElMessage.error('加载商品失败')
  }
}

const searchProduct = async () => {
  try {
    const params = new URLSearchParams()
    if (searchKeyword.value) {
      params.append('keyword', searchKeyword.value)
    }
    
    const response = await fetch(`/api/products?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    const result = await response.json()
    
    if (result.success) {
      products.value = result.data.products
    } else {
      ElMessage.error('搜索商品失败')
    }
  } catch (error) {
    console.error('Search products error:', error)
    ElMessage.error('搜索商品失败')
  }
}

const addToCart = (product) => {
  const existingItem = cartItems.value.find(item => item.id === product.id)
  
  if (existingItem) {
    if (existingItem.quantity < product.stock) {
      existingItem.quantity++
      existingItem.total = existingItem.quantity * existingItem.price
    } else {
      ElMessage.warning('库存不足')
    }
  } else {
    cartItems.value.push({
      ...product,
      quantity: 1,
      total: product.price
    })
  }
}

const removeFromCart = (index) => {
  cartItems.value.splice(index, 1)
}

const updateItemTotal = (index) => {
  const item = cartItems.value[index]
  item.total = item.quantity * item.price
}

const clearOrder = () => {
  cartItems.value = []
}

const checkout = async () => {
  if (cartItems.value.length === 0) {
    ElMessage.warning('购物车为空')
    return
  }
  
  try {
    const orderData = {
      items: cartItems.value.map(item => ({
        productId: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      totalAmount: totalAmount.value,
      paymentMethod: 'cash', // 默认现金支付
      status: 1 // 待支付
    }
    
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(orderData)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('订单创建成功')
      clearOrder()
    } else {
      ElMessage.error(result.message || '创建订单失败')
    }
  } catch (error) {
    console.error('Checkout error:', error)
    ElMessage.error('创建订单失败')
  }
}
</script>

<style scoped>
.pos-container {
  padding: 20px;
  height: 100vh;
  background: #f5f5f5;
}

.pos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.pos-info {
  display: flex;
  gap: 20px;
  color: #666;
}

.pos-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
  height: calc(100vh - 100px);
}

.product-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-bar {
  margin-bottom: 20px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.product-card {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.product-card:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.product-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.product-price {
  color: #e74c3c;
  font-size: 16px;
  margin-bottom: 5px;
}

.product-stock {
  color: #666;
  font-size: 12px;
}

.order-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-items {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.empty-cart {
  text-align: center;
  color: #999;
  padding: 40px 0;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.item-price {
  color: #e74c3c;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.item-total {
  font-weight: bold;
  color: #e74c3c;
  min-width: 60px;
}

.order-summary {
  border-top: 2px solid #f0f0f0;
  padding-top: 15px;
  margin-bottom: 20px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.total-amount {
  font-size: 18px;
  font-weight: bold;
  color: #e74c3c;
}

.payment-section {
  text-align: center;
}
</style>