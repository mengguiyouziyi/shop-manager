export interface Order {
  id: number
  order_number: string
  customer_name: string
  customer_phone: string
  total_amount: number
  status: number
  payment_status: number
  shop_id: number
  shop_name: string
  created_at: string
  notes?: string
}

export interface OrderCreate {
  customer_name: string
  customer_phone: string
  total_amount: number
  shop_id: number
  payment_method: string
  items: OrderItem[]
  notes?: string
}

export interface OrderUpdate {
  customer_name?: string
  customer_phone?: string
  total_amount?: number
  notes?: string
}

export interface OrderItem {
  product_id: number
  quantity: number
  price: number
}

export interface OrderStatus {
  status: number
}
