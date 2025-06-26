<template>
  <div>
    <el-table :data="orders" style="width: 100%">
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="order_date" label="订单日期" />
      <el-table-column prop="shipping_address" label="收货地址" />
      <el-table-column prop="payment_method" label="支付方式" />
      <el-table-column prop="user_id" label="用户 ID" />
      <el-table-column prop="total_amount" label="订单总额" />
      <el-table-column prop="status" label="订单状态" />
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getOrdersPaginated } from '@/api/index';

const orders = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);

const fetchOrders = async () => {
  try {
    const response = await getOrdersPaginated(currentPage.value, pageSize.value);
    orders.value = response.data.books;
    total.value = response.data.total;
  } catch (error) {
    console.error('获取订单列表失败:', error);
  }
};

const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  fetchOrders();
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchOrders();
};

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
/* 可添加自定义样式 */
</style>