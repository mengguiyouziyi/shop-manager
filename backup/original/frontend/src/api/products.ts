import { api } from './index'

// 商品类型定义
export interface Product {
  id: number
  name: string
  barcode: string
  price: number
  cost_price?: number
  stock: number
  unit: string
  category_id?: number
  shop_id: number
  status: number
  created_at: string
  updated_at?: string
}

export interface ProductCreate {
  name: string
  barcode: string
  price: number
  cost_price?: number
  stock: number
  unit: string
  category_id?: number
  shop_id: number
}

export interface ProductUpdate {
  name?: string
  barcode?: string
  price?: number
  cost_price?: number
  stock?: number
  unit?: string
  category_id?: number
  status?: number
}

// 商品API
export const productsApi = {
  // 获取商品列表
  getProducts: (params?: any) => {
    return api.get<Product[]>('/api/products/', { params })
  },

  // 获取单个商品
  getProduct: (id: number) => {
    return api.get<Product>(`/api/products/${id}`)
  },

  // 创建商品
  createProduct: (data: ProductCreate) => {
    return api.post<Product>('/api/products/', data)
  },

  // 更新商品
  updateProduct: (id: number, data: ProductUpdate) => {
    return api.put<Product>(`/api/products/${id}`, data)
  },

  // 删除商品
  deleteProduct: (id: number) => {
    return api.delete(`/api/products/${id}`)
  },

  // 批量更新库存
  updateStock: (data: { product_id: number; stock: number }[]) => {
    return api.post('/api/products/update-stock', data)
  },

  // 搜索商品
  searchProducts: (query: string) => {
    return api.get<Product[]>('/api/products/search', { params: { q: query } })
  },

  // 获取商品统计
  getProductStats: () => {
    return api.get('/api/products/stats')
  }
}
