<template>
  <div>
    <el-table :data="books" style="width: 100%">
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="title" label="书名" />
      <el-table-column prop="author" label="作者" />
      <el-table-column prop="publisher_id" label="出版社 ID" />
      <el-table-column prop="stock_quantity" label="库存数量" />
      <el-table-column prop="price" label="价格" />
      <el-table-column prop="rating" label="评分" />
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
import { getBooksPaginated } from '@/api/index'; // 替换为新 API

const books = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);

const fetchBooks = async () => {
  try {
    const response = await getBooksPaginated(currentPage.value, pageSize.value);
    books.value = response.data.books;
    total.value = response.data.total;
  } catch (error) {
    console.error('获取书籍库存列表失败:', error);
  }
};

const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  fetchBooks();
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchBooks();
};

onMounted(() => {
  fetchBooks();
});
</script>

<style scoped>
/* 可添加自定义样式 */
</style>