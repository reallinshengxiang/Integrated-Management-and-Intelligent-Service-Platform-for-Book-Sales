
<script setup>

import {reactive, ref} from "vue";
import {upload_url,auth} from "@/api";
import {ElMessage} from "element-plus";
import {useStore} from "vuex";

const store = useStore()
const ruleFormRef = ref()


const ruleForm = reactive({
  username:"",
  gender:"男",
  is_manager:'否',
  head_img:'',
  birthday:"",
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
  gender:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(['男','女'].indexOf(value) < 0){
          callback(new Error("用户名没有填写"))
        }
        callback()
      },
    }
  ],
  is_manager:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(['是','否'].indexOf(value) < 0){
          callback(new Error("用户名没有填写"))
        }
        callback()
      },
    }
  ],
  birthday:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        const dateReg = /^(\d{4})-(\d{2})-(\d{2})$/;

        if( !dateReg.test(value) ){
          callback(new Error('请输入正确的日期格式YYYY-MM-DD'))
          return false;
        }

        let date = {
          year : Number(RegExp.$1),
          month : Number(RegExp.$2),
          day : Number(RegExp.$3),
        }
        console.log(date)
        let dateObj = new Date(date.year, date.month-1, date.day);

        if( date.year !== dateObj.getFullYear() || date.month !== dateObj.getMonth()+1 || date.day !== dateObj.getDate() ){
          callback(new Error("日期不正确"))
          return false;
        }


        callback()
      },
    }
  ],
  password:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value.length < 6){
          callback(new Error("密码长度小于6"))
        }
        callback()
      },
    }
  ],
  checkPass:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value.length < 6){
          callback(new Error("密码长度小于6"))
        }
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

        <el-form-item prop="gender" label="性别">
          <el-radio-group v-model="ruleForm.gender" size="large">
            <el-radio-button label="男" />
            <el-radio-button label="女" />
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="is_manager" label="是否为管理员">
          <el-radio-group v-model="ruleForm.is_manager" size="large">
            <el-radio-button label="是"  />
            <el-radio-button label="否" />

          </el-radio-group>
        </el-form-item>
        <el-form-item prop="birthday" label="生日">
          <el-date-picker
              v-model="ruleForm.birthday"
              type="date"
              value-format="YYYY-MM-DD"
              size="large"
          />
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