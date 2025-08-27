<template>
  <div class="product-management-page">
    <div class="page-header">
      <h2>商品管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加商品
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="hover">
      <el-form :model="searchForm" inline>
        <el-form-item label="商品名称">
          <el-input
            v-model="searchForm.name"
            placeholder="输入商品名称"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="searchForm.category_id"
            placeholder="选择分类"
            clearable
            style="width: 150px"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 商品列表 -->
    <el-card class="table-card" shadow="hover">
      <div class="table-toolbar">
        <el-button
          type="danger"
          :disabled="selectedProducts.length === 0"
          @click="handleBatchDelete"
        >
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>

      <el-table
        :data="products"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="商品名称" min-width="200" />
        <el-table-column prop="barcode" label="条形码" width="150" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">
            ¥{{ row.price.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewProduct(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editProduct(row)">编辑</el-button>
            <el-button size="small" type="warning" @click="updateStock(row)">库存</el-button>
            <el-button size="small" type="danger" @click="deleteProduct(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑商品对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="isEdit ? '编辑商品' : '添加商品'"
      width="800px"
    >
      <el-form :model="productForm" :rules="productRules" ref="productFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品名称" prop="name">
              <el-input v-model="productForm.name" placeholder="输入商品名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="条形码" prop="barcode">
              <el-input v-model="productForm.barcode" placeholder="输入条形码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格" prop="price">
              <el-input-number
                v-model="productForm.price"
                :min="0"
                :precision="2"
                placeholder="输入价格"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="成本价" prop="cost_price">
              <el-input-number
                v-model="productForm.cost_price"
                :min="0"
                :precision="2"
                placeholder="输入成本价"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="库存" prop="stock">
              <el-input-number
                v-model="productForm.stock"
                :min="0"
                placeholder="输入库存"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单位" prop="unit">
              <el-input v-model="productForm.unit" placeholder="输入单位" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category_id">
              <el-select
                v-model="productForm.category_id"
                placeholder="选择分类"
                style="width: 100%"
              >
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="productForm.status" placeholder="选择状态" style="width: 100%">
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="productForm.description"
            type="textarea"
            :rows="3"
            placeholder="输入商品描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 库存更新对话框 -->
    <el-dialog v-model="showStockDialog" title="更新库存" width="400px">
      <el-form :model="stockForm" :rules="stockRules" ref="stockFormRef" label-width="80px">
        <el-form-item label="商品名称">
          <el-input :value="selectedProduct?.name" disabled />
        </el-form-item>
        <el-form-item label="当前库存">
          <el-input :value="selectedProduct?.stock" disabled />
        </el-form-item>
        <el-form-item label="新库存" prop="stock">
          <el-input-number
            v-model="stockForm.stock"
            :min="0"
            placeholder="输入新库存"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showStockDialog = false">取消</el-button>
          <el-button type="primary" @click="handleStockUpdate">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, Delete, Download } from '@element-plus/icons-vue'
import { productsApi } from '@/api/products'
import type { Product, ProductCreate, ProductUpdate } from '@/api/products'

// 响应式数据
const loading = ref(false)
const products = ref<Product[]>([])
const categories = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const showAddDialog = ref(false)
const showStockDialog = ref(false)
const isEdit = ref(false)
const editingProduct = ref<Product | null>(null)
const selectedProduct = ref<Product | null>(null)
const selectedProducts = ref<Product[]>([])
const productFormRef = ref()
const stockFormRef = ref()

// 搜索表单
const searchForm = reactive({
  name: '',
  category_id: undefined as number | undefined,
  status: undefined as number | undefined
})

// 商品表单
const productForm = reactive({
  name: '',
  barcode: '',
  price: 0,
  cost_price: 0,
  stock: 0,
  unit: '个',
  category_id: 1,
  status: 1,
  description: '',
  shop_id: 1
})

// 库存表单
const stockForm = reactive({
  stock: 0
})

// 表单验证规则
const productRules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  barcode: [{ required: true, message: '请输入条形码', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const stockRules = {
  stock: [{ required: true, message: '请输入新库存', trigger: 'blur' }]
}

// 方法
const loadProducts = async () => {
  loading.value = true
  try {
    const response = await productsApi.getProducts({
      page: currentPage.value,
      limit: pageSize.value,
      ...searchForm
    })
    products.value = response
    total.value = response.length
  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('加载商品失败')
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    // 暂时使用模拟数据
    categories.value = [
      { id: 1, name: '电子产品' },
      { id: 2, name: '服装鞋帽' },
      { id: 3, name: '食品饮料' },
      { id: 4, name: '家居用品' }
    ]
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadProducts()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    name: '',
    category_id: undefined,
    status: undefined
  })
  handleSearch()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadProducts()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadProducts()
}

const handleSelectionChange = (selection: Product[]) => {
  selectedProducts.value = selection
}

const viewProduct = (product: Product) => {
  console.log('查看商品:', product)
}

const editProduct = (product: Product) => {
  isEdit.value = true
  editingProduct.value = product
  Object.assign(productForm, {
    name: product.name,
    barcode: product.barcode,
    price: product.price,
    cost_price: product.cost_price || 0,
    stock: product.stock,
    unit: product.unit,
    category_id: product.category_id || 1,
    status: product.status,
    description: ''
  })
  showAddDialog.value = true
}

const deleteProduct = async (product: Product) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除商品"${product.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await productsApi.deleteProduct(product.id)
    ElMessage.success('商品删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除商品失败:', error)
      ElMessage.error('删除商品失败')
    }
  }
}

const handleBatchDelete = async () => {
  if (selectedProducts.value.length === 0) {
    ElMessage.warning('请选择要删除的商品')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedProducts.value.length} 个商品吗？`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedProducts.value.map(p => p.id)
    for (const id of ids) {
      await productsApi.deleteProduct(id)
    }
    
    ElMessage.success('批量删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

const updateStock = (product: Product) => {
  selectedProduct.value = product
  stockForm.stock = product.stock
  showStockDialog.value = true
}

const handleStockUpdate = async () => {
  if (!selectedProduct.value) return

  try {
    await productsApi.updateProduct(selectedProduct.value.id, {
      stock: stockForm.stock
    })
    ElMessage.success('库存更新成功')
    showStockDialog.value = false
    loadProducts()
  } catch (error) {
    console.error('更新库存失败:', error)
    ElMessage.error('更新库存失败')
  }
}

const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

const resetForm = () => {
  editingProduct.value = null
  Object.assign(productForm, {
    name: '',
    barcode: '',
    price: 0,
    cost_price: 0,
    stock: 0,
    unit: '个',
    category_id: 1,
    status: 1,
    description: ''
  })
}

const handleSubmit = async () => {
  try {
    if (isEdit.value && editingProduct.value) {
      await productsApi.updateProduct(editingProduct.value.id, productForm as ProductUpdate)
      ElMessage.success('商品更新成功')
    } else {
      await productsApi.createProduct(productForm as ProductCreate)
      ElMessage.success('商品添加成功')
    }
    
    showAddDialog.value = false
    loadProducts()
    resetForm()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请重试')
  }
}

// 生命周期
onMounted(() => {
  loadProducts()
  loadCategories()
})
</script>

<style scoped>
.product-management-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.table-toolbar {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
