<script setup>

import {reactive, watch, onBeforeMount, computed, ref} from "vue";
import {book, borrow, return_bookcopy, user} from "../../api";
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";

const router = useRouter();

const tableData = ref([])
const editFormRef = ref()
const total = ref(0)
const create_time = ref([null,null])
const return_time = ref([null,null])
const real_return_time = ref([null,null])
const dialogEditFormVisible = ref(false)

const form = reactive({
  page_num:1,
  page_size:10,
  username:"",
  create_time: '',
  return_time: '',
  real_return_time: ''
})

const editForm = reactive({
  id:'',
  username:"",
  bookcopy_id:"",
  return_time: '',
  real_return_time: ''
})

watch(create_time, (newVal,oldVal)=>{
  form.create_time = newVal.join(',')
})

watch(return_time, (newVal,oldVal)=>{
  form.return_time = newVal.join(',')
})

watch(real_return_time, (newVal,oldVal)=>{
  form.real_return_time = newVal.join(',')
})


watch(form,(newVal,oldVal)=>{
  console.log(newVal)
})


const handleEdit = (index, row)=>{
  editForm.username = row.user.username;
  editForm.id =row.id;
  editForm.bookcopy_id =row.bookcopy_id;
  editForm.real_return_time = row.real_return_time;
  editForm.return_time = row.return_time;
}

const handleDelete = (index, row)=>{
  borrow.delete({id:row.id}).then(({data})=>{
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

const onResetSubmit = async ()=>{
  form.username = "";
  form.book_title = "";
  form.create_time = '';
  create_time.value = [null, null];
  form.return_time = '';
  return_time.value = [null, null];
  form.real_return_time = '';
  real_return_time.value = [null, null];
}

const onSubmit = async ()=>{
  borrow.get(form).then(({data})=>{
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

const editSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      borrow.post({},editForm,{}).then(({data})=>{
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

const return_book = async (id)=>{
  return_bookcopy({id}).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    dialogEditFormVisible.value = false;
    onSubmit()
  }).catch(err=>{
    ElMessage.error(err)
  })
}

onBeforeMount(()=>{
  onSubmit()
})

const role_data = (rule, value, callback)=>{
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
}

const rules = reactive({
  username:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("租借者用户名"))
        }
        callback()
      },
    }
  ],
  bookcopy_id:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("book copy id没有填写"))
        }
        callback()
      },
    }
  ],
  return_time:[
    {trigger: 'blur' ,
      validator:role_data,
    }
  ],
  real_return_time:[
    {trigger: 'blur' ,
      validator:role_data,
    }
  ],
})

</script>

<template>

  <el-dialog v-model="dialogEditFormVisible" :title="'Edit Borrow:'+editForm.title">
    <el-form :rules="rules" ref="editFormRef" :model="editForm" label-width="100px">
      <el-form-item prop="username" label="租借者用户名">
        <el-input v-model="editForm.username" placeholder="Title" size="large"/>
      </el-form-item>
      <el-form-item prop="bookcopy_id" label="BookCopy Id">
        <el-input-number v-model="editForm.bookcopy_id" placeholder="BookCopy Id" size="large"/>
      </el-form-item>

      <el-form-item prop="return_time" label="预计归还日期">
        <el-date-picker
            v-model="editForm.return_time"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
      </el-form-item>

      <el-form-item prop="real_return_tim" label="实际归还日期">
        <el-date-picker
            v-model="editForm.real_return_time"
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
        <el-form-item label="用户名">
        <el-input v-model="form.username" placeholder="Username" />
      </el-form-item>

      <el-form-item label="租界日期范围">
        <el-date-picker
            v-model="create_time"
            type="daterange"
            range-separator="到"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item label="真实归还日期范围">
        <el-date-picker
            v-model="real_return_time"
            type="daterange"
            range-separator="到"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item label="预计归还日期范围">
        <el-date-picker
            v-model="return_time"
            type="daterange"
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
        <el-button type="success" @click="router.push({name:'index',params:{type:'book'}})">新建</el-button>
      </el-form-item>
    </el-form>
    <el-table
        :data="tableData"
        style="width: 100%"
    >
      <el-table-column prop="id" label="id" />
      <el-table-column label="用户名" >
        <template #default="scope">
            {{ scope.row.user.username }}
        </template>
      </el-table-column>
      <el-table-column label="书名:副本id" >
        <template #default="scope">
            {{ scope.row.book.title }} : <span style="color:  #85ce61">{{ scope.row.bookcopy_id }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="租出日期" />
      <el-table-column prop="return_time" label="预计归还日期" />
      <el-table-column prop="real_return_time" label="真实归还日期" />
      <el-table-column label="归还">
        <template #default="scope">
          <el-button size="small" type="success" @click="return_book(scope.row.id)" :disabled="scope.row.real_return_time !== ''" text>归还</el-button>

        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="dialogEditFormVisible = true;handleEdit(scope.$index, scope.row)"
          >Edit</el-button>
          <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
          >Delete</el-button>
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