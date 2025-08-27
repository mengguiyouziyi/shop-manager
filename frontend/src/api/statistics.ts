import { api } from './index'

// 统计数据类型定义
export interface DashboardStats {
  total_sales: number
  total_orders: number
  total_products: number
  total_members: number
  recent_orders: any[]
  top_products: any[]
}

export interface SalesStats {
  date: string
  sales: number
  orders: number
  customers: number
}

export interface ProductStats {
  product_id: number
  product_name: string
  quantity_sold: number
  revenue: number
  profit: number
}

export interface MemberStats {
  member_id: number
  member_name: string
  total_spent: number
  order_count: number
  last_order_date: string
}

export interface CategoryStats {
  category_id: number
  category_name: string
  product_count: number
  total_sales: number
}

// 统计API
export const statisticsApi = {
  // 获取仪表板统计
  getDashboardStats: () => {
    return api.get<DashboardStats>('/api/statistics/dashboard')
  },

  // 获取销售统计
  getSalesStats: (params?: any) => {
    return api.get<SalesStats[]>('/api/statistics/sales', { params })
  },

  // 获取商品销售统计
  getProductStats: (params?: any) => {
    return api.get<ProductStats[]>('/api/statistics/products', { params })
  },

  // 获取会员消费统计
  getMemberStats: (params?: any) => {
    return api.get<MemberStats[]>('/api/statistics/members', { params })
  },

  // 获取分类统计
  getCategoryStats: () => {
    return api.get<CategoryStats[]>('/api/statistics/categories')
  },

  // 获取收入统计
  getRevenueStats: (params?: any) => {
    return api.get('/api/statistics/revenue', { params })
  },

  // 获取利润统计
  getProfitStats: (params?: any) => {
    return api.get('/api/statistics/profit', { params })
  },

  // 获取库存预警
  getStockAlerts: () => {
    return api.get('/api/statistics/stock-alerts')
  },

  // 获取热销商品
  getHotProducts: (limit: number = 10) => {
    return api.get('/api/statistics/hot-products', { params: { limit } })
  },

  // 获取新会员统计
  getNewMembers: (days: number = 30) => {
    return api.get('/api/statistics/new-members', { params: { days } })
  },

  // 导出统计数据
  exportStats: (type: string, params?: any) => {
    return api.get(`/api/statistics/export/${type}`, { 
      params,
      responseType: 'blob'
    })
  }
}
