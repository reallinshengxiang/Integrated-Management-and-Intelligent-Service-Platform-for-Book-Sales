<template>
  <el-form :model="userForm" label-width="120px">
    <el-form-item label="ID">
      <el-input v-model="userForm.id" disabled></el-input>
    </el-form-item>
    <el-form-item label="用户名">
      <el-input v-model="userForm.username"></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="userForm.password" type="password"></el-input>
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="userForm.email"></el-input>
    </el-form-item>
    <el-form-item label="电话">
      <el-input v-model="userForm.phone"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="updateUserInfo">修改用户信息</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { userDetail } from '@/api/index'; 
import { useStore } from 'vuex';
import { updateUser } from '@/api/index';

const router=useRouter();
const store = useStore();
const userForm = ref({ 
  id: 0,
  username: '', 
  password: '', 
  email: '', 
  phone: '', 
});

onMounted(async () => { 
  if (store.state.modifyid === -1) { 
    store.state.modifyid = store.state.id; 
  }
  userForm.value.id = store.state.modifyid;
  const userId = store.state.modifyid;
  if (userId) { 
    try { 
      const api = userDetail(userId); 
      const response = await api.get();  
      userForm.value = { ...userForm.value, ...response.data }; 
    } catch (error) { 
      console.error('获取用户信息失败:', error); 
    } 
    console.log('inform:', userForm.username);
  } 
});

const updateUserInfo = async () => {
  try {
    const response = await updateUser(userForm.value);
    console.log('用户信息更新成功:', response.data);
    router.push(`/index/user`);
    // 可添加更新成功后的提示或跳转逻辑
  } catch (error) {
    console.error('用户信息更新失败:', error);
  }
};
</script>

<style scoped>
</style>