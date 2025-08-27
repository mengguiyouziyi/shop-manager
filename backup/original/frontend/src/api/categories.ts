import { api } from './index'

// 分类类型定义
export interface Category {
  id: number
  name: string
  parent_id: number
  sort_order: number
  shop_id: number
  status: number
  created_at: string
  updated_at?: string
  children?: Category[]
  product_count?: number
}

export interface CategoryCreate {
  name: string
  parent_id?: number
  sort_order?: number
  shop_id: number
}

export interface CategoryUpdate {
  name?: string
  parent_id?: number
  sort_order?: number
  status?: number
}

// 分类API
export const categoriesApi = {
  // 获取分类列表
  getCategories: (params?: any) => {
    return api.get<Category[]>('/api/categories/', { params })
  },

  // 获取单个分类
  getCategory: (id: number) => {
    return api.get<Category>(`/api/categories/${id}`)
  },

  // 创建分类
  createCategory: (data: CategoryCreate) => {
    return api.post<Category>('/api/categories/', data)
  },

  // 更新分类
  updateCategory: (id: number, data: CategoryUpdate) => {
    return api.put<Category>(`/api/categories/${id}`, data)
  },

  // 删除分类
  deleteCategory: (id: number) => {
    return api.delete(`/api/categories/${id}`)
  },

  // 获取分类树结构
  getCategoryTree: () => {
    return api.get<Category[]>('/api/categories/tree')
  },

  // 获取子分类
  getSubCategories: (parentId: number) => {
    return api.get<Category[]>(`/api/categories/${parentId}/children`)
  },

  // 更新分类排序
  updateCategoryOrder: (data: { id: number; sort_order: number }[]) => {
    return api.post('/api/categories/update-order', data)
  },

  // 获取分类统计
  getCategoryStats: () => {
    return api.get('/api/categories/stats')
  }
}
