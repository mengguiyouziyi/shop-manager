export interface Member {
  id: number
  name: string
  phone: string
  level: number
  points: number
  total_spent: number
  status: number
  shop_id: number
  shop_name: string
  created_at: string
  notes?: string
}

export interface MemberCreate {
  name: string
  phone: string
  level: number
  status: number
  shop_id: number
  notes?: string
}

export interface MemberUpdate {
  name?: string
  phone?: string
  level?: number
  status?: number
  notes?: string
}

export interface PointsAdjustment {
  points: number
  reason: string
}
