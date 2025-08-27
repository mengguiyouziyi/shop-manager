// 临时注释掉，避免编译错误
// import { request } from '@/utils/request'

export interface SystemSettings {
  app_name: string
  version: string
  timezone: string
  language: string
  maintenance_mode: boolean
}

export interface SecuritySettings {
  require_uppercase: boolean
  require_lowercase: boolean
  require_numbers: boolean
  require_symbols: boolean
  min_password_length: number
  password_expire_days: number
  max_login_attempts: number
  session_timeout: number
}

export interface NotificationSettings {
  email_enabled: boolean
  smtp_host: string
  smtp_port: number
  email_username: string
  email_password: string
  sms_enabled: boolean
  sms_api_key: string
}

export interface BackupSettings {
  auto_backup: boolean
  backup_frequency: string
  backup_retention: number
  backup_path: string
}

export const settingsApi = {
  // 获取系统设置
  getSystemSettings() {
    return Promise.resolve({} as SystemSettings)
  },

  // 更新系统设置
  updateSystemSettings(settings: Partial<SystemSettings>) {
    return Promise.resolve({} as SystemSettings)
  },

  // 获取安全设置
  getSecuritySettings() {
    return Promise.resolve({} as SecuritySettings)
  },

  // 更新安全设置
  updateSecuritySettings(settings: Partial<SecuritySettings>) {
    return Promise.resolve({} as SecuritySettings)
  },

  // 获取通知设置
  getNotificationSettings() {
    return Promise.resolve({} as NotificationSettings)
  },

  // 更新通知设置
  updateNotificationSettings(settings: Partial<NotificationSettings>) {
    return Promise.resolve({} as NotificationSettings)
  },

  // 获取备份设置
  getBackupSettings() {
    return Promise.resolve({} as BackupSettings)
  },

  // 更新备份设置
  updateBackupSettings(settings: Partial<BackupSettings>) {
    return Promise.resolve({} as BackupSettings)
  },

  // 创建备份
  createBackup() {
    return Promise.resolve({})
  },

  // 获取备份列表
  getBackupList() {
    return Promise.resolve([])
  },

  // 恢复备份
  restoreBackup(backupId: string) {
    return Promise.resolve({})
  },

  // 删除备份
  deleteBackup(backupId: string) {
    return Promise.resolve({})
  }
}
