<script setup>

import LoginHeaderBar from "@/conponents/LoginHeaderBar.vue";
import LoginForm from "@/conponents/login_forms/LoginForm.vue";
import RegisterForm from "@/conponents/login_forms/RegisterForm.vue";

const props = defineProps({
  login: {
    type:String,
    default: 'login'
  },
})


</script>

<template>
  <el-container>
    <el-header>
      <LoginHeaderBar />
    </el-header>
    <el-main>
      <LoginForm v-if="props.login === 'login'" />
      <RegisterForm v-if="props.login === 'register'" />
    </el-main>
  </el-container>
</template>



<style lang="scss" scoped>


.el-header,.el-footer{
  padding: 0;
}

.el-container{
  @include home-main();
}
</style>