export interface Product {
  id: number
  name: string
  barcode: string
  category_id: number
  category_name: string
  price: number
  stock: number
  unit: string
  status: number
  shop_id: number
  shop_name: string
  created_at: string
  description?: string
}

export interface ProductCreate {
  name: string
  barcode: string
  category_id: number
  price: number
  stock: number
  unit: string
  status: number
  shop_id: number
  description?: string
}

export interface ProductUpdate {
  name?: string
  barcode?: string
  category_id?: number
  price?: number
  stock?: number
  unit?: string
  status?: number
  description?: string
}

export interface StockAdjustment {
  stock: number
  reason: string
}
