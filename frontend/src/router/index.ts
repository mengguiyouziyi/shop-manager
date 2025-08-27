import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import Dashboard from '@/views/Dashboard.vue'
import Products from '@/views/Products.vue'
import Categories from '@/views/Categories.vue'
import Orders from '@/views/Orders.vue'
import Members from '@/views/Members.vue'
import POS from '@/views/POS.vue'
import Statistics from '@/views/Statistics.vue'
import Settings from '@/views/Settings.vue'
import UserManagement from '@/views/UserManagement.vue'
import UserProfile from '@/views/UserProfile.vue'
import ShopManagement from '@/views/ShopManagement.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'products',
        name: 'Products',
        component: Products
      },
      {
        path: 'categories',
        name: 'Categories',
        component: Categories
      },
      {
        path: 'orders',
        name: 'Orders',
        component: Orders
      },
      {
        path: 'members',
        name: 'Members',
        component: Members
      },
      {
        path: 'pos',
        name: 'POS',
        component: POS
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: Statistics
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement
      },
      {
        path: 'shops',
        name: 'ShopManagement',
        component: ShopManagement
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: UserProfile
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router