<script setup>

import {reactive, watch, onBeforeMount, computed, ref} from "vue";
import {author, user} from "../../api";
import {useRoute} from "vue-router";
import {ElMessage} from "element-plus";


const tableData = ref([])

const route = useRoute();

const form = reactive({
  page_size:10,
  page_um:1,
  name:"",
  birthday:"",
})

const addForm = reactive({
  name:"",
  birthday:"",
})

const editForm = reactive({
  id:"",
  name:"",
  birthday:"",
})

const total = ref(1)
const addFormRef = ref()
const editFormRef = ref()
const birthday_range = ref([null,null])
const dialogFormVisible = ref(false)
const dialogEditFormVisible = ref(false)

watch(form, (n,o)=>{
  route.query.page_num = n.page_num
})

watch(birthday_range ,(newVal,oldVal)=>{
  form.birthday = newVal.join(',')
})

watch(form,(newVal,oldVal)=>{
  console.log(newVal)
})

const handleEdit = (index, row)=>{
  Object.assign(editForm,row)
  editForm.birthday = row.birthday.split(" ")[0]
  console.log(editForm)
}


const handleDelete = (index, row)=>{
  author.delete({id:row.id}).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    ElMessage.success("删除成功")
    onSubmit()
  }).catch(err=>{
    ElMessage.error(err)
  })
}

const editSubmit = async (form) => {
  console.log(form)
  form.validate((valid) => {
    if (valid) {
      author.post({},editForm,{}).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        dialogEditFormVisible.value = false;
        onSubmit()
      }).catch(err=>{
        ElMessage.error(err)
      })
    } else {
      ElMessage.error('error submit!')
      return false
    }
  })
}

const onResetSubmit = async ()=>{
  form.name = "";
  form.birthday = '';

}

const onSubmit = async ()=>{
  author.get(form).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    tableData.value = data.data.infos;
    total.value = data.data.total;
  }).catch(err=>{
    ElMessage.error(err)
  })
}

const addSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      author.put({},addForm,{}).then(({data})=>{
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
        ElMessage.error(err)
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
  name:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
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

})

</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="Add Author">
    <el-form :rules="rules" ref="addFormRef" :model="addForm" label-width="100px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="addForm.name" placeholder="Username" size="large"/>
      </el-form-item>

      <el-form-item prop="birthday" label="生日日期">
        <el-date-picker
            v-model="addForm.birthday"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
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

  <el-dialog v-model="dialogEditFormVisible" :title="'Edit Author:'+editForm.name">
    <el-form :rules="rules" ref="editFormRef" :model="editForm" label-width="100px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="editForm.name" placeholder="Name" size="large"/>
      </el-form-item>

      <el-form-item prop="birthday" label="生日日期">
        <el-date-picker
            v-model="editForm.birthday"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
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
      <el-form-item label="姓名">
        <el-input v-model="form.name" placeholder="Name" />
      </el-form-item>
      <el-form-item label="生日日期范围">
        <el-date-picker
            v-model="birthday_range"
            type="daterange"
            range-separator="到"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
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
      <el-table-column prop="id" label="id" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="birthday" label="生日" />
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

.pagination{
  padding: 20px;
  background-color: #fff;
}

</style>