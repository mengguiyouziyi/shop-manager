<template>
  <div class="member-list">
    <div class="page-header">
      <h2>会员管理</h2>
      <el-button type="primary" @click="addMember">添加会员</el-button>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索会员姓名或手机号"
        style="width: 300px"
        @input="handleSearch"
      />
    </div>

    <el-table :data="members" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="points" label="积分" width="100" />
      <el-table-column prop="balance" label="余额" width="120">
        <template #default="scope">
          ¥{{ scope.row.balance }}
        </template>
      </el-table-column>
      <el-table-column prop="level" label="等级" width="100">
        <template #default="scope">
          <el-tag type="primary">{{ scope.row.level || '普通会员' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="birthday" label="生日" width="120">
        <template #default="scope">
          {{ scope.row.birthday || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
            {{ scope.row.status === 1 ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button size="small" @click="viewMember(scope.row)">查看</el-button>
          <el-button size="small" @click="editMember(scope.row)">编辑</el-button>
          <el-button size="small" type="success" @click="rechargeMember(scope.row)">充值</el-button>
        </template>
      </el-table-column>
    </el-table>

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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const members = ref([])

onMounted(() => {
  loadMembers()
})

const loadMembers = async () => {
  loading.value = true
  try {
    // 模拟API调用
    setTimeout(() => {
      members.value = [
        {
          id: 1,
          name: '张三',
          phone: '13900139000',
          points: 100,
          balance: 50.00,
          level: '普通会员',
          birthday: '1990-01-01',
          status: 1,
          created_at: '2024-01-01 00:00:00'
        },
        {
          id: 2,
          name: '李四',
          phone: '13900139001',
          points: 200,
          balance: 100.00,
          level: 'VIP会员',
          birthday: '1985-05-15',
          status: 1,
          created_at: '2024-01-02 00:00:00'
        }
      ]
      total.value = members.value.length
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('加载会员失败')
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const handleSearch = () => {
  currentPage.value = 1
  loadMembers()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadMembers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadMembers()
}

const addMember = () => {
  router.push('/members/add')
}

const viewMember = (member: any) => {
  ElMessage.info('查看会员详情功能开发中')
}

const editMember = (member: any) => {
  router.push(`/members/edit/${member.id}`)
}

const rechargeMember = (member: any) => {
  ElMessage.info('充值功能开发中')
}
</script>

<style scoped>
.member-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  text-align: right;
}
</style>