<script setup>

</script>

<template>
  <div class="home-header-bar">
      <span class="title">
        登陆 or 注册
      </span>
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


}

</style>