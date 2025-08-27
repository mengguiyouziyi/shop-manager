// 侧边栏菜单数据结构定义
export interface MenuItem {
  path: string
  name: string
  icon: string
  children?: MenuItem[]
  permission?: string[]
  meta?: {
    title?: string
    requiresAuth?: boolean
    keepAlive?: boolean
  }
}

// 菜单分组配置
export const menuGroups: { title: string; items: MenuItem[] }[] = [
  {
    title: '工作台',
    items: [
      {
        path: '/dashboard',
        name: '仪表盘',
        icon: 'Monitor',
        meta: { title: '仪表盘', requiresAuth: true }
      }
    ]
  },
  {
    title: '系统管理',
    items: [
      {
        path: '/users',
        name: '用户管理',
        icon: 'User',
        meta: { title: '用户管理', requiresAuth: true },
        permission: ['admin']
      },
      {
        path: '/shops',
        name: '店铺管理',
        icon: 'Shop',
        meta: { title: '店铺管理', requiresAuth: true },
        permission: ['admin', 'manager']
      },
      {
        path: '/settings',
        name: '系统设置',
        icon: 'Settings',
        meta: { title: '系统设置', requiresAuth: true },
        permission: ['admin']
      },
      {
        path: '/profile',
        name: '个人资料',
        icon: 'UserCircle',
        meta: { title: '个人资料', requiresAuth: true }
      }
    ]
  },
  {
    title: '商品管理',
    items: [
      {
        path: '/products',
        name: '商品管理',
        icon: 'Package',
        meta: { title: '商品管理', requiresAuth: true },
        children: [
          {
            path: '/products/list',
            name: '商品列表',
            icon: 'List',
            meta: { title: '商品列表', requiresAuth: true }
          },
          {
            path: '/products/categories',
            name: '分类管理',
            icon: 'FolderTree',
            meta: { title: '分类管理', requiresAuth: true }
          },
          {
            path: '/products/inventory',
            name: '库存管理',
            icon: 'Warehouse',
            meta: { title: '库存管理', requiresAuth: true }
          }
        ]
      },
      {
        path: '/categories',
        name: '分类管理',
        icon: 'FolderTree',
        meta: { title: '分类管理', requiresAuth: true }
      }
    ]
  },
  {
    title: '订单管理',
    items: [
      {
        path: '/orders',
        name: '订单管理',
        icon: 'ClipboardList',
        meta: { title: '订单管理', requiresAuth: true },
        children: [
          {
            path: '/orders/list',
            name: '订单列表',
            icon: 'ListOrdered',
            meta: { title: '订单列表', requiresAuth: true }
          },
          {
            path: '/orders/statistics',
            name: '订单统计',
            icon: 'BarChart3',
            meta: { title: '订单统计', requiresAuth: true }
          }
        ]
      }
    ]
  },
  {
    title: '会员管理',
    items: [
      {
        path: '/members',
        name: '会员管理',
        icon: 'Users',
        meta: { title: '会员管理', requiresAuth: true },
        children: [
          {
            path: '/members/list',
            name: '会员列表',
            icon: 'UserCheck',
            meta: { title: '会员列表', requiresAuth: true }
          },
          {
            path: '/members/levels',
            name: '会员等级',
            icon: 'Award',
            meta: { title: '会员等级', requiresAuth: true }
          }
        ]
      }
    ]
  },
  {
    title: '数据统计',
    items: [
      {
        path: '/statistics',
        name: '数据统计',
        icon: 'BarChart',
        meta: { title: '数据统计', requiresAuth: true },
        children: [
          {
            path: '/statistics/sales',
            name: '销售统计',
            icon: 'TrendingUp',
            meta: { title: '销售统计', requiresAuth: true }
          },
          {
            path: '/statistics/traffic',
            name: '流量分析',
            icon: 'Eye',
            meta: { title: '流量分析', requiresAuth: true }
          }
        ]
      }
    ]
  },
  {
    title: '收银台',
    items: [
      {
        path: '/pos',
        name: 'POS收银',
        icon: 'CreditCard',
        meta: { title: 'POS收银', requiresAuth: true },
        permission: ['admin', 'cashier']
      }
    ]
  }
]

// 获取扁平化的菜单项（用于权限检查）
export const getFlatMenuItems = (): MenuItem[] => {
  const flatItems: MenuItem[] = []
  
  const flatten = (items: MenuItem[]) => {
    items.forEach(item => {
      flatItems.push(item)
      if (item.children) {
        flatten(item.children)
      }
    })
  }
  
  menuGroups.forEach(group => {
    flatten(group.items)
  })
  
  return flatItems
}

// 根据角色过滤菜单
export const filterMenuByRole = (userRole: string): { title: string; items: MenuItem[] }[] => {
  const hasPermission = (item: MenuItem): boolean => {
    if (!item.permission) return true
    return item.permission.includes(userRole)
  }
  
  const filterItems = (items: MenuItem[]): MenuItem[] => {
    return items
      .filter(hasPermission)
      .map(item => ({
        ...item,
        children: item.children ? filterItems(item.children) : undefined
      }))
      .filter(item => item.children?.length || !item.children)
  }
  
  return menuGroups
    .map(group => ({
      ...group,
      items: filterItems(group.items)
    }))
    .filter(group => group.items.length > 0)
}

// 查找当前激活的菜单项
export const findActiveMenuItem = (currentPath: string): MenuItem | null => {
  const flatItems = getFlatMenuItems()
  return flatItems.find(item => item.path === currentPath) || null
}