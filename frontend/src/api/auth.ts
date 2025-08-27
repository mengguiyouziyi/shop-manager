import { api } from './index'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: number
    username: string
    name: string
    role: string
    phone?: string
    shop_id: number
    status: number
    last_login: string
    created_at: string
  }
}

export interface UserProfile {
  id: number
  username: string
  name: string
  phone?: string
  role: string
  shop_id: number
  status: number
  last_login: string
  created_at: string
  updated_at?: string
}

export interface ChangePasswordRequest {
  current_password: string
  new_password: string
}

export interface UpdateProfileRequest {
  name?: string
  phone?: string
}

export const authApi = {
  // 用户登录
  login: (data: LoginRequest): Promise<LoginResponse> => {
    return api.post<LoginResponse>('/api/auth/login', data)
  },

  // 用户注册
  register: (data: any): Promise<any> => {
    return api.post('/api/auth/register', data)
  },

  // 获取当前用户信息
  getCurrentUser: (): Promise<UserProfile> => {
    return api.get<UserProfile>('/api/auth/me')
  },

  // 更新用户资料
  updateProfile: (data: UpdateProfileRequest): Promise<UserProfile> => {
    return api.put<UserProfile>('/api/auth/profile', data)
  },

  // 修改密码
  changePassword: (data: ChangePasswordRequest): Promise<any> => {
    return api.post('/api/auth/change-password', data)
  },

  // 刷新token
  refreshToken: (): Promise<any> => {
    return api.post('/api/auth/refresh')
  },

  // 用户登出
  logout: (): Promise<any> => {
    return api.post('/api/auth/logout')
  },

  // 忘记密码
  forgotPassword: (email: string): Promise<any> => {
    return api.post('/api/auth/forgot-password', { email })
  },

  // 重置密码
  resetPassword: (token: string, newPassword: string): Promise<any> => {
    return api.post('/api/auth/reset-password', { token, new_password: newPassword })
  }
}