<template>
  <div class="user-management-container">
    <!-- 标题部分 -->
    <div class="page-title">
      <h1>用户管理</h1>
      <!-- 饼图容器 -->
      <div class="pie-chart-container">
        <div id="user-count-pie-chart" style="width: 300px; height: 300px;"></div>
      </div>
    </div>
    <!-- 表格部分 -->
    <el-table :data="users" style="width: 100%" stripe border>
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="username" label="用户名" width="200" />
      <el-table-column prop="email" label="邮箱" width="300" />
      <el-table-column prop="phone" label="电话" width="300" />
      <el-table-column prop="user_type" label="角色" />
      <el-table-column label="操作" width="80">
        <template #default="{ row }">
          <el-button type="primary" @click="goToModify(row.id)" class="action-button">修改</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页器部分 -->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getUsersPaginated } from '@/api/index'; 
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';
import * as echarts from 'echarts';

const router = useRouter();
const store = useStore();

const users = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const userCount = ref(null);

const fetchUsers = async () => {
  try {
    const response = await getUsersPaginated(currentPage.value, pageSize.value);
    users.value = response.data.users;
    total.value = response.data.total;
  } catch (error) {
    console.error('获取用户列表失败:', error);
  }
};

const fetchUserCount = async () => {
  try {
    const response = await axios.get('/api/users/count');
    userCount.value = response.data;
    // 绘制饼图
    drawPieChart();
  } catch (error) {
    console.error('获取用户统计信息失败:', error);
  }
};

const drawPieChart = () => {
  if (userCount.value) {
    const chartDom = document.getElementById('user-count-pie-chart');
    const myChart = echarts.init(chartDom);
    const option = {
      title: {
        text: '用户类型分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          name: '用户数量',
          type: 'pie',
          radius: '50%',
          data: [
            { 
              value: userCount.value.admin_count, 
              name: '管理员',
              itemStyle: {
                color: 'rgb(51, 63, 114)' // 管理员扇形颜色
              }
            },
            { 
              value: userCount.value.customer_count, 
              name: '普通用户',
              itemStyle: {
                color: '#66b1ff' // 普通用户扇形颜色
              }
            }
          ]
        }
      ]
    };
    myChart.setOption(option);
  }
};

const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  fetchUsers();
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchUsers();
};

const goToModify = (id) => {
  store.dispatch('set_modifyid', id);
  router.push(`/index/modify`);
};

onMounted(() => {
  fetchUsers();
  fetchUserCount();
});
</script>

<style scoped>
/* 容器样式 */
.user-management-container {
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  max-width: 1200px;
  transition: all 0.3s ease;
}

.user-management-container:hover {
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.15);
}

/* 标题样式 */
.page-title {
  text-align: center;
  margin-bottom: 20px;
}

.page-title h1 {
  font-size: 32px;
  color: #333;
  font-weight: 600;
}

/* 饼图容器样式 */
.pie-chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

/* 表格样式 */
.el-table {
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.el-table__header-wrapper th {
  background-color: #f0f5ff;
  color: #333;
  font-weight: 600;
  padding: 15px;
  text-align: center;
  vertical-align: middle;
  border-bottom: 1px solid #e0e0e0;
}

.el-table__body-wrapper td {
  padding: 15px;
  text-align: center;
  vertical-align: middle;
  border-bottom: 1px solid #e0e0e0;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #fafafa;
}

.el-table__body tr:hover td {
  background-color: #e5f6ff;
}

/* 操作按钮样式 */
.action-button {
  background-color:rgb(51, 63, 114);
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #66b1ff;
}

/* 分页器样式 */
.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination .el-pagination__sizes .el-input .el-input__inner {
  border-radius: 5px;
}

.pagination .el-pager li {
  border-radius: 5px;
  margin: 0 5px;
  transition: all 0.3s ease;
}

.pagination .el-pager li:hover {
  background-color: #f0f5ff;
}

.pagination .el-pager li.active {
  background-color: #409eff;
  color: #fff;
}
</style>