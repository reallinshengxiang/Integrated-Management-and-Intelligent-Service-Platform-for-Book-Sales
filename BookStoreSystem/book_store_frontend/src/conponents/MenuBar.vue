
<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRoute } from "vue-router"
import {
  User,
  EditPen,
  Collection,
  Share,
  Position,
  Location
} from '@element-plus/icons-vue'

const route = useRoute()

const isCollapse = ref(false)

onBeforeMount(()=>{
  console.log(route.path)
})

</script>


<template>
  <el-col>
    <el-menu
        class="menu-bar"
        :collapse="isCollapse"
        active-text-color="#fff"
        :unique-opened="true"
        :router="true"
        popper-effect="dark"
        :default-active="route.path"

    >
      <el-menu-item class="title" disabled>
        <img src="../assets/vite.svg" />
        <span :style="!isCollapse ? {paddingLeft:'10px'} : {}">图书管理系统</span>
      </el-menu-item>
<!--      <el-sub-menu>-->
<!--        <template #title>-->
<!--            <el-icon><location /></el-icon>-->
<!--            <span>Base Controll</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/index/borrow-book">-->
<!--            <el-icon><User /></el-icon>-->
<!--            <span>借用图书</span>-->
<!--          </el-menu-item>-->
<!--          <el-menu-item index="/index/pay">-->
<!--            <el-icon><User /></el-icon>-->
<!--            <span>逾期支付</span>-->
<!--          </el-menu-item>-->
<!--      </el-sub-menu>-->
      <el-menu-item index="/index/user">
        <el-icon><User /></el-icon>
        <span>用户管理</span>
      </el-menu-item>
      <el-menu-item index="/index/author">
        <el-icon><EditPen /></el-icon>
        <span>作者管理</span>
      </el-menu-item>
      <el-menu-item index="/index/book">
        <el-icon><Collection /></el-icon>
        <span>图书管理</span>
      </el-menu-item>
      <el-menu-item index="/index/book-copy">
        <el-icon><Collection /></el-icon>
        <span>图书副本管理</span>
      </el-menu-item>
      <el-menu-item index="/index/borrow">
        <el-icon><Share /></el-icon>
        <span>租借管理</span>
      </el-menu-item>
      <el-menu-item index="/index/about">
        <el-icon><Position /></el-icon>
        <span>关于我们</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>

<style lang="scss" scoped>

.el-menu-item.is-disabled{
  opacity: unset;


}


.el-col{
  height: 100%;
}

.title{
  @include menu-logo();
  height: 60px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  >span{}

}

.menu-bar{
  @include menu-bar();
  height: 100%;
}


.el-menu-item{
  @include menu-item();
}

</style>

<style>
.el-menu[role='menu']{
  --el-menu-active-color:rgba(0,0,0,0);
  background-color: rgba(0,0,0,0)
}

.el-sub-menu__title:hover{
  background-color: rgba(0,0,0,.05);
}

</style>
