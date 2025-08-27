<template>
  <div class="product-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑商品' : '添加商品' }}</h2>
      <el-button @click="goBack">返回</el-button>
    </div>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="product-form-content"
    >
      <el-form-item label="商品名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入商品名称" />
      </el-form-item>

      <el-form-item label="商品条码" prop="barcode">
        <el-input v-model="formData.barcode" placeholder="请输入商品条码" />
      </el-form-item>

      <el-form-item label="商品分类" prop="category_id">
        <el-select v-model="formData.category_id" placeholder="请选择分类">
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="售价" prop="price">
        <el-input-number
          v-model="formData.price"
          :precision="2"
          :step="0.1"
          :min="0"
        />
      </el-form-item>

      <el-form-item label="成本价" prop="cost_price">
        <el-input-number
          v-model="formData.cost_price"
          :precision="2"
          :step="0.1"
          :min="0"
        />
      </el-form-item>

      <el-form-item label="库存数量" prop="stock">
        <el-input-number
          v-model="formData.stock"
          :min="0"
          :step="1"
        />
      </el-form-item>

      <el-form-item label="单位" prop="unit">
        <el-input v-model="formData.unit" placeholder="如：包、个、瓶" />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="formData.status">
          <el-radio :label="1">正常</el-radio>
          <el-radio :label="0">停用</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="商品描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请输入商品描述"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const formRef = ref()
const loading = ref(false)
const categories = ref([])

const isEdit = computed(() => !!route.params.id)

const formData = reactive({
  name: '',
  barcode: '',
  category_id: '',
  price: 0,
  cost_price: 0,
  stock: 0,
  unit: '',
  status: 1,
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' }
  ],
  barcode: [
    { required: true, message: '请输入商品条码', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入售价', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请输入单位', trigger: 'blur' }
  ]
}

onMounted(() => {
  loadCategories()
  if (isEdit.value) {
    loadProduct()
  }
})

const loadCategories = async () => {
  try {
    // 模拟API调用
    categories.value = [
      { id: 1, name: '食品' },
      { id: 2, name: '饮料' },
      { id: 3, name: '日用品' }
    ]
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const loadProduct = async () => {
  try {
    const productId = route.params.id
    // 模拟API调用
    setTimeout(() => {
      const productData = {
        id: productId,
        name: '方便面',
        barcode: '6901028089685',
        category_id: 1,
        price: 5.50,
        cost_price: 4.00,
        stock: 100,
        unit: '包',
        status: 1,
        description: '美味的方便面'
      }
      
      Object.assign(formData, productData)
    }, 500)
  } catch (error) {
    ElMessage.error('加载商品信息失败')
  }
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 模拟API调用
    setTimeout(() => {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      router.push('/products')
    }, 1000)
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

const goBack = () => {
  router.push('/products')
}
</script>

<style scoped>
.product-form {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.product-form-content {
  max-width: 600px;
  margin: 0 auto;
}
</style>