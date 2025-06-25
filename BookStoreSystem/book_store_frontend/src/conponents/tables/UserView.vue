<script setup>

import {reactive, watch, onBeforeMount, computed, ref} from "vue";
import { useRoute } from 'vue-router';
import { user } from "../../api";
import {ElMessage} from "element-plus";
import {upload_url} from "@/api";
import {useStore} from "vuex";

const store = useStore()

const route = useRoute();

let tableData = ref([])

const form = reactive({
  username:"",
  gender:"全部",
  birthday:[null,null],
  is_manager:"全部"
})

const total = ref(1)

const getToken = ()=>{
  return store.state.token;
}

const addForm = reactive({
  username:"",
  gender:"男",
  is_manager:'否',
  head_img:'',
  birthday:"",
  password:""
})

const addFormRef = ref()

const editForm = reactive({
  username:"",
  gender:"男",
  is_manager:'否',
  head_img:'',
  birthday:"",
  password:""
})

const editFormRef = ref()

const birthday_range = ref([null,null])

watch(form, (n,o)=>{
  route.query.page_num = n.page_num
})

watch(birthday_range ,(newVal,oldVal)=>{
  form.birthday = newVal.join(',')
})

const handleEdit = (index, row)=>{
  Object.assign(editForm,row)
  editForm.gender = editForm.gender ? "男" : "女";
  editForm.is_manager = editForm.is_manager ? "是" : "否";
  editForm.birthday = row.birthday.split(" ")[0]
  console.log(editForm)
}


const handleDelete = (index, row)=>{
  user.delete({id:row.id}).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    ElMessage.success("删除成功")
    onSubmit()
  }).catch(err=>{
    ElMessage.error(String(err))
  })
}
let dialogFormVisible = ref(false)
let dialogEditFormVisible = ref(false)


const onSubmit = async ()=>{
  user.get(form).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    tableData.value = data.data.infos;
    total.value = data.data.total;
  }).catch(err=>{
    ElMessage.error(String(err))
  })
}


const onResetSubmit = async ()=>{
  form.username = "";
  form.gender = "全部";
  form.birthday = [null,null];
  form.is_manager = "全部";
  await onSubmit();
}

const editSubmit = async (form) => {
  console.log(form)
  form.validate((valid) => {
    if (valid) {
      user.post({},editForm,{}).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        dialogEditFormVisible.value = false;
        onSubmit()
      }).catch(err=>{
        ElMessage.error(String(err))
      })
    } else {
      ElMessage.error('error submit!')
      return false
    }
  })
}

const addSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      user.put({},addForm,{}).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        console.log(data)
        total.value += 1;
        dialogFormVisible.value = false;

        if(tableData.value.length >=10) return;
        tableData.value.push(data.data)
      }).catch(err=>{
        ElMessage.error(String(err))
      })
    } else {
      ElMessage.error('error submit!')
      return false
    }
  })

}

onBeforeMount(()=>{
  onSubmit()
})

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
  ]
})

const handleAvatarSuccess = (
    response,
    uploadFile
) => {
  addForm.head_img = import.meta.env.VITE_APP_BASE_API+response.data.filename
}

const handleAvatarSuccessEdit = (
    response,
    uploadFile
) => {
  editForm.head_img = import.meta.env.VITE_APP_BASE_API+response.data.filename
}

const beforeAvatarUpload = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

</script>

<template>

  <el-dialog v-model="dialogFormVisible" title="Add User">
    <el-form :rules="rules" ref="addFormRef" :model="addForm" label-width="100px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="addForm.username" placeholder="Username" size="large"/>
      </el-form-item>
      <el-form-item label="头像">
        <el-upload
            class="avatar-uploader"
            :action="upload_url"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :headers="{Authorization:getToken()}"
        >
          <img v-if="addForm.head_img" :src="addForm.head_img" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item prop="gender" label="性别">
        <el-radio-group v-model="addForm.gender" size="large">
          <el-radio-button label="男" />
          <el-radio-button label="女" />
        </el-radio-group>
      </el-form-item>
      <el-form-item prop="is_manager" label="是否为管理员">
        <el-radio-group v-model="addForm.is_manager" size="large">
          <el-radio-button label="是"  />
          <el-radio-button label="否" />

        </el-radio-group>
      </el-form-item>
      <el-form-item prop="birthday" label="生日">
        <el-date-picker
            v-model="addForm.birthday"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-input v-model="addForm.password" size="large" type="password" placeholder="Please input" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addSubmit(addFormRef)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog v-model="dialogEditFormVisible" :title="'Edit User:'+editForm.username">
    <el-form :rules="rules" ref="editFormRef" :model="editForm" label-width="100px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="editForm.username" placeholder="Username" size="large"/>
      </el-form-item>
      <el-form-item label="头像">
        <el-upload
            class="avatar-uploader"
            :action="upload_url"
            :show-file-list="false"
            :on-success="handleAvatarSuccessEdit"
            :before-upload="beforeAvatarUpload"
            :headers="{Authorization:getToken()}"
        >
          <img v-if="editForm.head_img" :src="editForm.head_img" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item prop="gender" label="性别">
        <el-radio-group v-model="editForm.gender" size="large">
          <el-radio-button label="男" />
          <el-radio-button label="女" />
        </el-radio-group>
      </el-form-item>
      <el-form-item prop="is_manager" label="是否为管理员">
        <el-radio-group v-model="editForm.is_manager" size="large">
          <el-radio-button label="是"  />
          <el-radio-button label="否" />

        </el-radio-group>
      </el-form-item>
      <el-form-item prop="birthday" label="生日">
        <el-date-picker
            v-model="editForm.birthday"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-input v-model="editForm.password" size="large" type="password" placeholder="Please input" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogEditFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="editSubmit(editFormRef)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <div class="user-view">

    <el-form :inline="true" :model="form" class="demo-form-inline">
      <el-form-item label="用户名">
        <el-input v-model="form.username" placeholder="Username" />
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="form.gender" size="large">
          <el-radio-button label="男" />
          <el-radio-button label="女" />
          <el-radio-button label="全部" />

        </el-radio-group>
      </el-form-item>
      <el-form-item label="是否为管理员">
        <el-radio-group v-model="form.is_manager" size="large">
          <el-radio-button label="是"  />
          <el-radio-button label="否" />
          <el-radio-button label="全部" />

        </el-radio-group>
      </el-form-item>
      <el-form-item label="生日日期范围">
        <el-date-picker
            v-model="birthday_range"
            type="daterange"
            value-format="YYYY-MM-DD"
            range-separator="到"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onResetSubmit">重置并查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="success" @click="dialogFormVisible = true">新建</el-button>
      </el-form-item>
    </el-form>
    <el-table
        :data="tableData"
        style="width: 100%"
    >
      <el-table-column prop="id" label="id" width="180" />
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="gender" :formatter="(row, column, cellValue, index)=>{return cellValue ? '男' : '女'}" label="性别" width="180" />
      <el-table-column prop="birthday" label="生日" />
      <el-table-column prop="is_manager" :formatter="(row, column, cellValue, index)=>{return cellValue ? '是' : '否'}" label="是否为管理员" />
      <el-table-column prop="head_img" label="头像" />

      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="dialogEditFormVisible = true;handleEdit(scope.$index, scope.row)"
          >Edit</el-button
          >
          <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
          >Delete</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination @current-change="onSubmit()" :page-size="form.page_size" v-model:current-page="form.page_num"  background layout="prev, pager, next" :total="total" />
    </div>
  </div>
</template>

<style lang="scss" scoped>

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}

.pagination{
  padding: 20px;
  background-color: #fff;
}

</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>

