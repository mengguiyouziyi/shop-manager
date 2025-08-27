import { api } from './index'

export interface ShopCreate {
  name: string
  address?: string
  phone?: string
  license_key?: string
}

export interface ShopUpdate {
  name?: string
  address?: string
  phone?: string
  license_key?: string
  status?: number
}

export interface ShopResponse {
  id: number
  name: string
  address?: string
  phone?: string
  license_key?: string
  status: number
  created_at: string
  updated_at?: string
}

export interface ShopList {
  items: ShopResponse[]
  total: number
  skip: number
  limit: number
  has_more: boolean
}

export interface ShopStats {
  shop_id: number
  shop_name: string
  user_count: number
  status: number
  created_at: string
}

export const shopApi = {
  // 获取店铺列表
  getShops: (params?: {
    skip?: number
    limit?: number
    status?: number
  }): Promise<ShopList> => {
    return api.get('/api/shops/', { params })
  },

  // 获取指定店铺
  getShop: (id: number): Promise<ShopResponse> => {
    return api.get(`/api/shops/${id}`)
  },

  // 创建店铺
  createShop: (data: ShopCreate): Promise<ShopResponse> => {
    return api.post('/api/shops/', data)
  },

  // 更新店铺
  updateShop: (id: number, data: ShopUpdate): Promise<ShopResponse> => {
    return api.put(`/api/shops/${id}`, data)
  },

  // 删除店铺
  deleteShop: (id: number): Promise<{ message: string }> => {
    return api.delete(`/api/shops/${id}`)
  },

  // 获取店铺统计信息
  getShopStats: (id: number): Promise<ShopStats> => {
    return api.get(`/api/shops/${id}/stats`)
  }
}
