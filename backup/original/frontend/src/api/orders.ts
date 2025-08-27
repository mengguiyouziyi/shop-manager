import { api } from './index'

// 订单类型定义
export interface OrderItem {
  id: number
  order_id: number
  product_id: number
  quantity: number
  price: number
  total_price: number
  product?: {
    id: number
    name: string
    barcode: string
    unit: string
  }
}

export interface Order {
  id: number
  order_no: string
  shop_id: number
  member_id?: number
  total_amount: number
  discount_amount: number
  payment_method: string
  payment_status: number
  status: number
  operator_id?: number
  remark?: string
  created_at: string
  updated_at?: string
  items: OrderItem[]
  member?: {
    id: number
    name: string
    phone: string
  }
  operator?: {
    id: number
    username: string
    name: string
  }
}

export interface OrderCreate {
  shop_id: number
  member_id?: number
  discount_amount?: number
  payment_method: string
  remark?: string
  items: {
    product_id: number
    quantity: number
    price: number
  }[]
}

export interface OrderUpdate {
  status?: number
  payment_status?: number
  payment_method?: string
  remark?: string
}

// 订单API
export const ordersApi = {
  // 获取订单列表
  getOrders: (params?: any) => {
    return api.get<Order[]>('/api/orders/', { params })
  },

  // 获取单个订单
  getOrder: (id: number) => {
    return api.get<Order>(`/api/orders/${id}`)
  },

  // 创建订单
  createOrder: (data: OrderCreate) => {
    return api.post<Order>('/api/orders/', data)
  },

  // 更新订单
  updateOrder: (id: number, data: OrderUpdate) => {
    return api.put<Order>(`/api/orders/${id}`, data)
  },

  // 删除订单
  deleteOrder: (id: number) => {
    return api.delete(`/api/orders/${id}`)
  },

  // 获取订单统计
  getOrderStats: () => {
    return api.get('/api/orders/stats')
  },

  // 获取今日订单
  getTodayOrders: () => {
    return api.get<Order[]>('/api/orders/today')
  },

  // 获取待处理订单
  getPendingOrders: () => {
    return api.get<Order[]>('/api/orders/pending')
  },

  // 更新订单状态
  updateOrderStatus: (id: number, status: number) => {
    return api.patch(`/api/orders/${id}/status`, { status })
  },

  // 更新支付状态
  updatePaymentStatus: (id: number, payment_status: number) => {
    return api.patch(`/api/orders/${id}/payment`, { payment_status })
  }
}
