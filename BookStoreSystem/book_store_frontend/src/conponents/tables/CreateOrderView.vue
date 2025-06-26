<template>
  <div>
    <el-table :data="orderItems" style="width: 100%">
      <el-table-column prop="bookName" label="书名">
        <template #default="{ row }">
          <el-autocomplete
            v-model="row.bookName"
            :fetch-suggestions="(queryString, cb) => fetchBooksByTitle(queryString, cb, row)"
            placeholder="输入书名"
            @select="(item) => handleBookSelect(item, row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="isbn" label="ISBN">
        <template #default="{ row }">
          <el-autocomplete
            v-model="row.isbn"
            :fetch-suggestions="(queryString, cb) => fetchBooksByISBN(queryString, cb, row)"
            placeholder="输入ISBN号"
            @select="(item) => handleISBNSelect(item, row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="price" label="书籍单价" />
      <el-table-column prop="quantity" label="订购数量">
        <template #default="{ row }">
          <el-input-number v-model="row.quantity" :min="0" />
        </template>
      </el-table-column>
      <el-table-column label="订购总价">
        <template #default="{ row }">
          {{ (row.quantity * row.price).toFixed(2) }}
        </template>
      </el-table-column>
    </el-table>
    <el-button @click="addRow">订购更多图书</el-button>
    <el-button @click="submitOrder">提交订单</el-button>
    <div style="text-align: right; margin-top: 10px;">
      <span style="color: #333;">订单总价: {{ (calculateTotalPrice()).toFixed(2) }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { searchBooksByTitle, searchBooksByISBN, createOrder } from '@/api/index';

const orderItems = ref([
  { bookName: '', isbn: '', price: 0.0, quantity: 0, id:0 }
]);

const addRow = () => {
  orderItems.value.push({ bookName: '', isbn: '', price: 0.0, quantity: 0, id:0});
};

const fetchBooksByTitle = (queryString, cb, row) => {
  if (queryString) {
    searchBooksByTitle(queryString).then(response => {
      const results = response.data;
      if (Array.isArray(results)) {
      cb(results.map(item => ({ value: item.title, ...item })));
    } else {
      console.error('Expected results to be an array, but got:', results);
      cb([]);
    }
    }).catch(error => {
      console.error('搜索书名失败:', error);
      cb([]);
    });
  } else {
    cb([]);
  }
};

const fetchBooksByISBN = (queryString, cb, row) => {
  if (queryString) {
    searchBooksByISBN(queryString).then(response => {
      const results = response.data;
      if (Array.isArray(results)) {
      cb(results.map(item => ({ value: item.isbn, ...item })));
    } else {
      console.error('Expected results to be an array, but got:', results);
      cb([]);
    }
    }).catch(error => {
      console.error('搜索ISBN失败:', error);
      cb([]);
    });
  } else {
    cb([]);
  }
};

const handleBookSelect = (item, row) => {
  row.bookName = item.title;
  row.isbn = item.isbn;
  row.price = item.price;
  row.quantity = 1;
  row.id = item.id;
};

const handleISBNSelect = (item, row) => {
  row.isbn = item.isbn;
  row.bookName = item.title;
  row.price = item.price;
  row.quantity = 1;
  row.id = item.id;
};

const calculateTotalPrice = () => {
  return orderItems.value.reduce((total, item) => total + (item.quantity * item.price), 0);
};

const store = useStore();

const submitOrder = async () => {
  const user_id = store.state.id;
  const shipping_address = '';
  const payment_method = '';
  const order_items = orderItems.value.map(item => ({
    book_id: item.id, // 假设存在 bookId 字段，根据实际情况调整
    quantity: item.quantity,
    unit_price: item.price
  }));

  const orderData = {
    user_id,
    shipping_address,
    payment_method,
    order_items
  };

  try {
    const response = await createOrder(orderData);
    console.log('订单提交成功:', response);
    // 可以添加提交成功后的逻辑，如清空表单等
  } catch (error) {
    console.error('订单提交失败:', error);
  }
};
</script>

<style scoped>
/* 可以添加样式 */
</style>