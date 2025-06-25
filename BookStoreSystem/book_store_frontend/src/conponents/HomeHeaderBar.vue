<script setup>

import {useRoute, useRouter} from "vue-router";
import {useStore} from "vuex";

const route = useRoute()
const store = useStore()
const router = useRouter()

console.log(route.path)

const logout = ()=>{
  store.dispatch('reset')
  router.go(0)
}

const getTitle = (key)=>{
  switch (key) {
    case '/index/author' : return "作者管理"
    case '/index/user' : return "用户管理"
    case '/index/book' : return "图书管理"
    case '/index/borrow' : return "租借管理"
    case '/index/about' : return "关于我们"
    default : return ""
  }
}

</script>

<template>
    <div class="home-header-bar">
      <span class="title">
        {{getTitle(route.path)}}
      </span>
      <span @click="logout()" class="logout">退出登入:{{store.state.username}}</span>
    </div>
</template>

<style lang="scss" scoped>

.home-header-bar{
  @include home-header-bar();
  width: 80%;
  height: 100%;
  display: flex;
  padding: 0 10%;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgb(0 0 0 / 15%);
  z-index: 1;

  .title{
    @include home-header-title();
    padding-bottom: 7px;
  }

  .logout{
    @include home-header-text();

    cursor: pointer;
  }

}

</style>