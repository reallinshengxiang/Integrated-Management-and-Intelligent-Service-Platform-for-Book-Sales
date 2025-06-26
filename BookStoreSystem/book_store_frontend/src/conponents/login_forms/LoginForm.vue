
<script setup>

import {reactive, ref} from "vue";
import {ElMessage} from "element-plus";
import {auth} from "@/api";
import {useStore} from "vuex";
import {useRouter} from "vue-router";

const store = useStore();
const router = useRouter();
const ruleFormRef = ref()

const checkUsername = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入用户名'))
  } else {

    callback()
  }
}

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {

    callback()
  }
}


const ruleForm = reactive({
  password: '',
  username: '',
})

const rules = reactive({
  password: [{ validator: validatePass, trigger: 'blur' }],
  username: [{ validator: checkUsername, trigger: 'blur' }],
})

const submitForm = (formEl) => {
  if (!formEl) return
  console.log('开始登陆')
  formEl.validate((valid) => {
    if (valid) {
      console.log('登录表合法')
      auth.login(ruleForm).then((response) => {
        // 假设 response 是实际的响应对象
        const data = response.data;
        console.log('收到反响', data);
        // 这里假设后端返回的状态码通过 HTTP 状态码判断
        if (response.status !== 200) {
          console.log('错误处理')
          ElMessage.error('登录失败，请检查用户名和密码');
          return;
        }
        console.log('登陆验证成功')
        store.dispatch('set_username', ruleForm.username);
        store.dispatch('set_id', data.user_id);
        store.dispatch('set_token', data.token);
        ElMessage.success("登录成功")
        router.push({name:'home'});
      }).catch(err => {
        console.log('报错')
        ElMessage.error(String(err))
      })
    } else {
      console.log('表单问题')
      ElMessage.error("检查表单填写")
      return false
    }
  })
}

const resetForm = (formEl) => {
  if (!formEl) return
  formEl.resetFields()
}

</script>

<template>
  <el-card class="card">
    <template #header>
      <el-row align="middle" justify="space-between">
        <span class="title">登录</span>
        <span class="tips">没有账号? <el-link href="#/auth/register">前往注册</el-link></span>
      </el-row>
    </template>
    <template #default>
      <el-form
          ref="ruleFormRef"
          :model="ruleForm"
          status-icon
          :rules="rules"
          label-width="120px"
          class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model.number="ruleForm.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="ruleForm.password" type="password" autocomplete="off" />
        </el-form-item>


        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)"
          >Submit</el-button
          >
          <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
        </el-form-item>
      </el-form>
    </template>
  </el-card>
</template>


<style scoped>

.card{
  width: 100%;
  max-width: 1140px;
  margin: auto;
  margin-top: 30px;
}

.title{
  font-size: 25px;
  font-weight: bold;
}

.tips{
  font-size: 14px;
}

</style>