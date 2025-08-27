<template>
  <div class="product-list">
    <div class="page-header">
      <h2>商品管理</h2>
      <el-button type="primary" @click="handleAdd">添加商品</el-button>
    </div>
    
    <div class="search-bar">
      <el-input
        v-model="searchForm.name"
        placeholder="搜索商品名称或条码"
        style="width: 300px"
        @input="handleSearch"
      />
      <el-select v-model="searchForm.category_id" placeholder="选择分类" style="width: 200px" @change="handleSearch">
        <el-option label="全部分类" value="" />
        <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
      </el-select>
    </div>

    <el-table :data="products" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="商品名称" />
      <el-table-column prop="barcode" label="条码" width="120" />
      <el-table-column prop="category.name" label="分类" width="100" />
      <el-table-column prop="price" label="售价" width="100">
        <template #default="scope">
          ¥{{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="cost_price" label="成本价" width="100">
        <template #default="scope">
          ¥{{ scope.row.cost_price || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="unit" label="单位" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="pagination.current"
      v-model:page-size="pagination.pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :total="pagination.total"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Product, Category } from '@/types'

const router = useRouter()

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const searchForm = ref({
  name: '',
  category_id: undefined as number | undefined,
  status: undefined as number | undefined
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

onMounted(() => {
  loadProducts()
  loadCategories()
})

const loadProducts = () => {
  loading.value = true
  // 模拟数据加载
  setTimeout(() => {
    products.value = [
      {
        id: 1,
        name: '可口可乐',
        barcode: '123456789',
        category_id: 1,
        category: { id: 1, name: '饮料', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
        price: 3.50,
        cost_price: 2.80,
        stock: 100,
        unit: '瓶',
        status: 1,
        created_at: '2024-01-01 00:00:00'
      },
      {
        id: 2,
        name: '薯片',
        barcode: '123456790',
        category_id: 1,
        category: { id: 1, name: '食品', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
        price: 8.00,
        cost_price: 6.00,
        stock: 50,
        unit: '包',
        status: 1,
        created_at: '2024-01-01 00:00:00'
      },
      {
        id: 3,
        name: '矿泉水',
        barcode: '123456791',
        category_id: 2,
        category: { id: 2, name: '饮料', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
        price: 2.00,
        cost_price: 1.50,
        stock: 200,
        unit: '瓶',
        status: 1,
        created_at: '2024-01-01 00:00:00'
      },
      {
        id: 4,
        name: '纸巾',
        barcode: '123456792',
        category_id: 3,
        category: { id: 3, name: '日用品', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
        price: 5.00,
        cost_price: 3.50,
        stock: 80,
        unit: '包',
        status: 1,
        created_at: '2024-01-01 00:00:00'
      }
    ]
    loading.value = false
  }, 500)
}

const loadCategories = () => {
  categories.value = [
    { id: 1, name: '食品', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
    { id: 2, name: '饮料', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' },
    { id: 3, name: '日用品', parent_id: 0, parent_name: '', sort_order: 1, status: 1, created_at: '' }
  ]
}

const handleSearch = () => {
  pagination.value.current = 1
  loadProducts()
}

const handleReset = () => {
  searchForm.value = {
    name: '',
    category_id: undefined,
    status: undefined
  }
  handleSearch()
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  loadProducts()
}

const handleCurrentChange = (val: number) => {
  pagination.value.current = val
  loadProducts()
}

const handleAdd = () => {
  router.push('/products/add')
}

const handleEdit = (product: Product) => {
  router.push(`/products/edit/${product.id}`)
}

const handleDelete = async (product: Product) => {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    products.value = products.value.filter(p => p.id !== product.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消删除
  }
}

const handleStatusChange = (product: Product) => {
  product.status = product.status === 1 ? 0 : 1
  ElMessage.success('状态更新成功')
}

const getStatusText = (status: number) => {
  return status === 1 ? '上架' : '下架'
}

const getStatusType = (status: number) => {
  return status === 1 ? 'success' : 'info'
}
</script>

<style scoped>
.product-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  text-align: right;
}
</style>