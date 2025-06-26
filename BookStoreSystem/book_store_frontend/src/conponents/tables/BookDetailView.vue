<template>
  <div class="book-detail">
    <el-card class="book-detail-card">
      <div v-if="bookDetail.title">
        <p>ID: {{ bookDetail.id }}</p>
        <p>书名: {{ bookDetail.title }}</p>
        <p>作者: {{ bookDetail.author }}</p>
        <p>价格: {{ Number(bookDetail.price).toFixed(2) }}元</p>
        <p>评分: {{ bookDetail.rating }}</p>
        <p>描述: {{ bookDetail.description }}</p>
        <p>出版社ID: {{ bookDetail.publisher_id }}</p>
      </div>
      <div v-else>
        加载中...
      </div>
      <div id="rating-chart" style="width: 300px; height: 200px;"></div>
    </el-card>
    <!-- 新增评论分页展示 -->
    <el-card class="review-list-card">
      <template #header>
        <div class="card-header">
          <span>图书评论</span>
          <el-button type="primary" @click="dialogVisible = true">添加评论</el-button>
        </div>
      </template>
      <el-table :data="reviews">
        <el-table-column prop="id" label="评论ID" />
        <el-table-column prop="user_id" label="用户ID" />
        <el-table-column prop="rating" label="评分" />
        <el-table-column prop="comment" label="评论内容" />
      </el-table>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
      />
    </el-card>
    <el-dialog v-model="dialogVisible" title="添加评论">
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="评分">
          <el-select v-model="reviewForm.rating" placeholder="请选择评分">
            <el-option v-for="item in [1, 2, 3, 4, 5]" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="评论内容">
          <el-input v-model="reviewForm.comment" type="textarea" rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReview">提交</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 这里添加图书详情展示内容 -->
    <el-card class="recommendation-bar box-card">
      <template #header>
        <div class="card-header">
          <span>为您推荐</span>
        </div>
      </template>
      <div v-for="book in recommendedBooks" :key="book.id" class="recommendation-item">
        <div @click="setDetailIdAndRefresh(book.id)">{{ book.title }} - {{ book.author }}</div>
        <div>评分: {{ book.rating }}</div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { userRecommendation, getBookDetail, getReviewRatingStats, getReviewListPaginated, createReview } from '@/api/index.js'
import store from '@/store'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const bookId = ref(store.state.detailid)
const bookDetail = ref({
  id: '',
  title: '',
  price: 0,
  author: '',
  rating: 0,
  description: '',
  publisher_id: ''
})
const recommendedBooks = ref([])
const ratingStats = ref({})
const reviews = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const reviewForm = ref({
  rating: null,
  comment: ''
})

const setDetailIdAndRefresh = (id) => {
  console.log('click', id);
  store.dispatch('set_detailid', id);
  router.go(0)
}

const getReviews = async () => {
  try {
    const response = await getReviewListPaginated(bookId.value).post({},{
      page: currentPage.value,
      per_page: pageSize.value
    });
    
    reviews.value = response.data.reviews;
    total.value = response.data.total;
    console.log(reviews.value)
    
  } catch (error) {
    console.error('获取评论失败:', error);
  }
}

const handleCurrentChange = (page) => {
  currentPage.value = page;
  getReviews();
}

const submitReview = async () => {
  try {
    const userId = store.state.id
    const response = await createReview({
      user_id: userId,
      book_id: bookId.value,
      rating: reviewForm.value.rating,
      comment: reviewForm.value.comment
    })
    if (response.data) {
      dialogVisible.value = false
      reviewForm.value = { rating: null, comment: '' }
      await getReviews()
    }
  } catch (error) {
    console.error('添加评论失败:', error)
  }
}

onMounted(async () => {
  try {
    const response = await getBookDetail(bookId.value).get();
    if (response.data) {
      bookDetail.value = response.data;
    }
    const userId = store.state.id;
    console.log(userId)
    const recommendationResponse = await userRecommendation(userId).get();
    const bookIds = recommendationResponse.data["recommendation_list"];

    for (const id of bookIds) {
      const detailResponse = await getBookDetail(id).get();
      const bookInfo = detailResponse.data; // 假设书籍信息在 data 字段中
      recommendedBooks.value.push({
        id: id,
        title: bookInfo.title,
        author: bookInfo.author,
        rating: Number(bookInfo.rating).toFixed(1)
      });
    }

    const statsResponse = await getReviewRatingStats(bookId.value).get();
    if (statsResponse.data) {
      ratingStats.value = statsResponse.data;
      const chartDom = document.getElementById('rating-chart');
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: '评分分布'
        },
        grid: {
          left: 'auto',
          right: 10, // 修改为较小的值使图表靠近右边界
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: Object.keys(ratingStats.value)
        },
        yAxis: {
          type: 'value',
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { show: false },
          splitLine: { show: false }
        },
        series: [{ 
          data: Object.values(ratingStats.value),
          type: 'bar',
          label: { 
            show: true,
            position: 'top'
          }
        }]
      };
      myChart.setOption(option);
    }
    // 确保调用获取评论方法
    await getReviews();
  } catch (error) {
    console.error('获取数据失败:', error);
  }
})
</script>

<style lang="scss" scoped>
.book-detail {
  padding: 20px;
  position: relative;
}

.book-detail-card {
  position: static;
  width: calc(70% - 60px);
  margin-left: 40px;
  margin-right: 20px;
  text-align: left; // 添加内容靠左对齐样式
}

.recommendation-bar {
  position: fixed;
  top: auto;
  bottom: 80px;
  right: 20px;
  width: 20%;
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}

.recommendation-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-bottom: 1px solid #eee;
  padding: 16px 0;
}

.recommendation-item:last-child {
  border-bottom: none;
}

.card-header {
  display: flex;
  align-items: flex-start;
}

.book-detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-list-card {
  width: calc(70% - 60px);
  margin-left: 40px;
  margin-right: 20px;
}
</style>