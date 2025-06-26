<template>
    <el-card class="box-card">
        <template #header>
            <div class="card-header">
                <span>About Us</span>
                
            </div>
        </template>
        <el-col>
            <p class="content">
                图书管理系统,基于flask Restful API设计和vite+vue3的系统,组件库来自Element Plus。
                由西安交通大学林圣翔与仲星焱制作。
            </p>
        </el-col>
    </el-card>
</template>


<script setup>

</script>


<style lang="scss" scoped>

.card-header{
    display: flex;
    align-items: flex-start;
}

.content{
    text-align: start;
}

</style>