<template>
  <div class="sidebar-container" :class="{ collapsed: isCollapsed }">
    <!-- Logo 区域 -->
    <div class="sidebar-logo">
      <div class="logo-content">
        <span class="logo-icon">🏪</span>
        <span class="logo-text">店铺管理系统</span>
      </div>
    </div>

    <!-- Element Plus 菜单 -->
    <el-menu
      class="sidebar-menu"
      :default-active="activeMenu"
      :collapse="isCollapsed"
      :unique-opened="true"
      background-color="transparent"
      text-color="#ECF0F1"
      active-text-color="#409EFF"
      router
    >
      <!-- 动态渲染菜单分组 -->
      <template v-for="group in filteredMenuGroups" :key="group.title">
        <!-- 分组标题 -->
        <div v-if="!isCollapsed" class="menu-group-title">
          {{ group.title }}
        </div>

        <!-- 菜单项 -->
        <template v-for="item in group.items" :key="item.path">
          <!-- 有子菜单的情况 -->
          <el-sub-menu 
            v-if="item.children && item.children.length"
            :index="item.path"
            :class="{ 'menu-item-disabled': !hasPermission(item) }"
          >
            <template #title>
              <span class="menu-icon">
                {{ getIconText(item.icon) }}
              </span>
              <span>{{ item.name }}</span>
            </template>

            <!-- 子菜单项 -->
            <el-menu-item
              v-for="child in item.children"
              :key="child.path"
              :index="child.path"
              :class="{ 'menu-item-disabled': !hasPermission(child) }"
            >
              <span class="menu-icon">
                {{ getIconText(child.icon) }}
              </span>
              <span>{{ child.name }}</span>
            </el-menu-item>
          </el-sub-menu>

          <!-- 无子菜单的情况 -->
          <el-menu-item
            v-else
            :index="item.path"
            :class="{ 'menu-item-disabled': !hasPermission(item) }"
          >
            <span class="menu-icon">
              {{ getIconText(item.icon) }}
            </span>
            <span>{{ item.name }}</span>
          </el-menu-item>
        </template>
      </template>
    </el-menu>

    <!-- 折叠按钮 -->
    <button class="collapse-button" @click="toggleCollapse">
      <span class="collapse-icon">{{ isCollapsed ? '▶' : '◀' }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { menuGroups, filterMenuByRole, findActiveMenuItem } from './SidebarMenuData'
import './SidebarStyles.css'

const route = useRoute()
const authStore = useAuthStore()

// 侧边栏折叠状态
const isCollapsed = ref(false)

// 获取用户角色
const userRole = computed(() => authStore.user?.role || '')

// 根据角色过滤菜单
const filteredMenuGroups = computed(() => {
  return filterMenuByRole(userRole.value)
})

// 当前激活的菜单项
const activeMenu = computed(() => {
  return route.path
})

// 检查权限
const hasPermission = (item: any) => {
  if (!item.permission) return true
  return item.permission.includes(userRole.value)
}

// 获取图标文本
const getIconText = (iconName: string): string => {
  const iconMap: Record<string, string> = {
    'Monitor': '📊',
    'User': '👤',
    'Shop': '🏪',
    'Settings': '⚙️',
    'UserCircle': '👤',
    'Package': '📦',
    'FolderTree': '📁',
    'ClipboardList': '📋',
    'ListOrdered': '📝',
    'BarChart3': '📈',
    'Users': '👥',
    'UserCheck': '👤✓',
    'Award': '🏆',
    'BarChart': '📊',
    'TrendingUp': '📈',
    'Eye': '👁️',
    'CreditCard': '💳',
    'List': '📝',
    'Warehouse': '🏭'
  }
  return iconMap[iconName] || '📄'
}

// 切换折叠状态
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// 暴露方法供父组件调用
defineExpose({
  toggleCollapse,
  isCollapsed
})
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-logo {
  flex-shrink: 0;
}

.sidebar-menu {
  flex: 1;
  overflow-y: auto;
}

.collapse-button {
  flex-shrink: 0;
  margin: 16px auto;
}
</style>