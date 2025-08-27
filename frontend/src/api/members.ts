import { api } from './index'

// 会员类型定义
export interface Member {
  id: number
  name: string
  phone: string
  level_id: number
  points: number
  balance: number
  birthday?: string
  shop_id: number
  status: number
  created_at: string
  updated_at?: string
}

export interface MemberCreate {
  name: string
  phone: string
  level_id?: number
  points?: number
  balance?: number
  birthday?: string
  shop_id: number
}

export interface MemberUpdate {
  name?: string
  phone?: string
  level_id?: number
  points?: number
  balance?: number
  birthday?: string
  status?: number
}

export interface MemberLevel {
  id: number
  name: string
  discount_rate: number
  points_rate: number
  description?: string
}

// 会员API
export const membersApi = {
  // 获取会员列表
  getMembers: (params?: any) => {
    return api.get<Member[]>('/api/members/', { params })
  },

  // 获取单个会员
  getMember: (id: number) => {
    return api.get<Member>(`/api/members/${id}`)
  },

  // 创建会员
  createMember: (data: MemberCreate) => {
    return api.post<Member>('/api/members/', data)
  },

  // 更新会员
  updateMember: (id: number, data: MemberUpdate) => {
    return api.put<Member>(`/api/members/${id}`, data)
  },

  // 删除会员
  deleteMember: (id: number) => {
    return api.delete(`/api/members/${id}`)
  },

  // 搜索会员
  searchMembers: (query: string) => {
    return api.get<Member[]>('/api/members/search', { params: { q: query } })
  },

  // 根据手机号查找会员
  getMemberByPhone: (phone: string) => {
    return api.get<Member>(`/api/members/phone/${phone}`)
  },

  // 更新会员积分
  updatePoints: (id: number, points: number) => {
    return api.patch(`/api/members/${id}/points`, { points })
  },

  // 更新会员余额
  updateBalance: (id: number, balance: number) => {
    return api.patch(`/api/members/${id}/balance`, { balance })
  },

  // 获取会员等级列表
  getMemberLevels: () => {
    return api.get<MemberLevel[]>('/api/members/levels')
  },

  // 获取会员统计
  getMemberStats: () => {
    return api.get('/api/members/stats')
  }
}
