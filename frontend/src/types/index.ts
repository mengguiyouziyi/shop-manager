// 用户相关类型
export interface User {
  id: number
  username: string
  name: string
  email?: string
  role: string
  shop_id: number
  shop?: Shop
  created_at: string
}

// 店铺相关类型
export interface Shop {
  id: number
  name: string
  address?: string
  phone?: string
  status: number
}

// 商品相关类型
export interface Product {
  id: number
  name: string
  barcode: string
  category_id: number
  category: Category
  price: number
  cost_price: number
  stock: number
  unit: string
  status: number
  created_at: string
}

// 商品分类类型
export interface Category {
  id: number
  name: string
  parent_id: number
  parent_name: string
  sort_order: number
  status: number
  created_at: string
}

// 会员相关类型
export interface Member {
  id: number
  name: string
  phone: string
  points: number
  balance: number
  level: string
  birthday: string
  status: number
  created_at: string
}

// 订单相关类型
export interface Order {
  id: number
  order_no: string
  member_id?: number
  member?: Member
  total_amount: number
  discount_amount: number
  payment_method: string
  payment_status: number
  status: number
  created_at: string
  items: OrderItem[]
}

// 订单项类型
export interface OrderItem {
  id: number
  product_id: number
  product: Product
  quantity: number
  price: number
  total: number
}

// 购物车项类型
export interface CartItem {
  id: number
  name: string
  price: number
  stock: number
  quantity: number
  total: number
}

// 统计数据类型
export interface Statistics {
  todaySales: number
  salesGrowth: number
  todayOrders: number
  ordersGrowth: number
  todayCustomers: number
  customersGrowth: number
  avgOrder: number
  avgOrderDecline: number
}

// 销售趋势数据类型
export interface SalesTrend {
  date: string
  sales: number
  orders: number
  customers: number
  avg_order: number
}

// 系统日志类型
export interface SystemLog {
  time: string
  user: string
  action: string
  ip: string
  result: string
}

// 登录凭据类型
export interface LoginCredentials {
  shop_id: number
  username: string
  password: string
}

// API响应类型
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status: string
}

// 分页参数类型
export interface PaginationParams {
  page: number
  page_size: number
  search?: string
  category_id?: number
  status?: number
}

// 分页响应类型
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
