
<script setup>
import {reactive, ref} from "vue";
import {auth} from "@/api";
import {ElMessage} from "element-plus";
import {useStore} from "vuex";

const store = useStore()
const ruleFormRef = ref()


const ruleForm = reactive({
  username:"",
  password:"",
  checkPass:""
})


const submitForm = (formEl) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      auth.register(ruleForm).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        ElMessage.success("注册成功")
      }).catch(err=>{
        ElMessage.error(err)
      })
    } else {
      ElMessage.error("检查表单填写")
      return false
    }
  })
}

const resetForm = (formEl) => {
  if (!formEl) return
  formEl.resetFields()
}

const rules = reactive({
  username:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("用户名没有填写"))
        }
        callback()
      },
    }
  ],
  password:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("密码没有填写"))
        }
        callback()
      },
    }
  ],
  checkPass:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value !== ruleForm.password){
          callback(new Error("两次密码填写不一样"))
        }
        callback()
      },
    }
  ]
})
</script>

<template>
  <el-card class="card">
    <template #header>
      <el-row align="middle" justify="space-between">
        <span class="title">注册</span>
        <span class="tips">已有账号? <el-link href="#/auth/login">前往登录</el-link></span>
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
        <el-form-item prop="username" label="用户名">
          <el-input v-model="ruleForm.username" placeholder="Username" size="large"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="ruleForm.password" type="password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input
              v-model="ruleForm.checkPass"
              type="password"
              autocomplete="off"
          />
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