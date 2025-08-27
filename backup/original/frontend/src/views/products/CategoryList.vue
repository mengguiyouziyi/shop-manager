<template>
  <div class="category-list">
    <div class="page-header">
      <h2>商品分类</h2>
      <el-button type="primary" @click="addCategory">添加分类</el-button>
    </div>

    <el-table :data="categories" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="parent_id" label="父分类" width="100">
        <template #default="scope">
          {{ scope.row.parent_id === 0 ? '顶级分类' : scope.row.parent_name }}
        </template>
      </el-table-column>
      <el-table-column prop="sort_order" label="排序" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
            {{ scope.row.status === 1 ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editCategory(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteCategory(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const loading = ref(false)
const categories = ref([])

onMounted(() => {
  loadCategories()
})

const loadCategories = async () => {
  loading.value = true
  try {
    // 模拟API调用
    setTimeout(() => {
      categories.value = [
        {
          id: 1,
          name: '食品',
          parent_id: 0,
          parent_name: '',
          sort_order: 1,
          status: 1,
          created_at: '2024-01-01 00:00:00'
        },
        {
          id: 2,
          name: '饮料',
          parent_id: 0,
          parent_name: '',
          sort_order: 2,
          status: 1,
          created_at: '2024-01-01 00:00:00'
        },
        {
          id: 3,
          name: '日用品',
          parent_id: 0,
          parent_name: '',
          sort_order: 3,
          status: 1,
          created_at: '2024-01-01 00:00:00'
        }
      ]
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('加载分类失败')
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const addCategory = () => {
  ElMessage.info('添加分类功能开发中')
}

const editCategory = (category: any) => {
  ElMessage.info('编辑分类功能开发中')
}

const deleteCategory = async (category: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类"${category.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 模拟删除操作
    categories.value = categories.value.filter(c => c.id !== category.id)
    ElMessage.success('删除成功')
  } catch (error) {
    // 用户取消删除
  }
}
</script>

<style scoped>
.category-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>