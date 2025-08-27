export interface Category {
  id: number
  name: string
  parent_id: number
  parent_name?: string
  sort_order: number
  product_count: number
  status: number
  shop_id: number
  shop_name: string
  created_at: string
  description?: string
}

export interface CategoryCreate {
  name: string
  parent_id: number
  sort_order: number
  status: number
  shop_id: number
  description?: string
}

export interface CategoryUpdate {
  name?: string
  parent_id?: number
  sort_order?: number
  status?: number
  description?: string
}
