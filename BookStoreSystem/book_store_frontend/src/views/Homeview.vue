<script setup>
import HomeHeaderBar from "@/conponents/HomeHeaderBar.vue";
import MenuBar from "@/conponents/MenuBar.vue";
import Footer from "@/conponents/Footer.vue";
import UserView from "@/conponents/tables/UserView.vue";
import BookView from "@/conponents/tables/BookView.vue";
import OrderView from "@/conponents/tables/OrderView.vue";
import BookDetailView from "@/conponents/tables/BookDetailView.vue";
import CreateOrderView from "@/conponents/tables/CreateOrderView.vue";
import AIhelperView from "@/conponents/tables/AIhelperView.vue";
import AboutWe from "@/conponents/tables/AboutWe.vue";
import {onBeforeUpdate, computed} from "vue";
import {useRoute, useRouter} from "vue-router";
import ModifyUserView from '@/conponents/tables/ModifyUserView.vue';



const route = useRoute();

const props = defineProps({
  type: {
    type:String,
    default: 'user'
  },
})

let getQueryPage = computed(()=>{

  return props.type;
})

onBeforeUpdate(()=>{
})

const getView = computed(() => {
  if (getQueryPage.value === 'user') {
    return UserView;
  }
  if (getQueryPage.value === 'modify') {
    return ModifyUserView;
  }
  if (getQueryPage.value === 'book') {
    return BookView;
  }
  if (getQueryPage.value === 'order') {
    return OrderView;
  }
  if (getQueryPage.value === 'bookdetail') {
    return BookDetailView;
  }
  if (getQueryPage.value === 'ai-helper') {
    return AIhelperView;
  }
  if (getQueryPage.value === 'create-order') {
    return CreateOrderView;
  }
  if (getQueryPage.value === 'about') {
    return AboutWe;
  }
});
</script>
  
<template>
  <el-container class="">

    <el-aside width="200px"><MenuBar /></el-aside>
    <el-container>
      <el-header><HomeHeaderBar /></el-header>
      <el-main><component :is="getView" /></el-main>
      <el-footer><Footer /></el-footer>
    </el-container>
  </el-container>
</template>

<style lang="scss" scoped>

.el-header,.el-footer{
  padding: 0;
}

.el-main{
  @include home-main();
}


</style>
