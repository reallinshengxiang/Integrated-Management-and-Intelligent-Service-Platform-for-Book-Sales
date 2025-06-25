<script setup>

import {reactive, watch, onBeforeMount, computed, ref} from "vue";
import {author, book, book_copy, borrow, user} from "../../api";
import {ElMessage} from "element-plus";


const tableData = ref([])

const authors = reactive([

])

const form = reactive({
  title:"",
  author:[],
  release_time: "",
  price: "",
  isbn: ""
})

const addForm = reactive({
  title:"",
  author:[],
  release_time: "",
  price: "",
  isbn: ""
})

const editForm = reactive({
  id:"",
  title:"",
  author:[],
  release_time: "",
  price: "",
  isbn: ""
})

const addBorrow = reactive({
  user_id:"",
  book_id:"",
  return_time: '',
})

const addFormRef = ref()
const editFormRef = ref()
const addBorrowRef = ref()
const total = ref(1)
const release_time = ref([null,null])
const price = reactive([null,null])
const dialogFormVisible = ref(false)
const dialogAddBorrowFormVisible = ref(false)
const dialogEditFormVisible = ref(false)

watch(release_time,(newVal,oldVal)=>{
  form.release_time = newVal.join(",")
})

watch(price,(newVal,oldVal)=>{
  console.log(newVal)
  form.price = newVal.join(",")
})

watch(form,(newVal,oldVal)=>{
  console.log(newVal)
})

const changeMin = (currentValue)=>{
    if(currentValue > price[1]){
      price[1] = currentValue;
    }
}


const handleEdit = (index, row)=>{
  Object.assign(editForm,row)
  editForm.author = []
  for(var i=0;i<row.author.length;i++){
    editForm.author[i] = row.author[i].id
  }

}


const handleDelete = (index, row)=>{
  book.delete({id:row.id}).then(({data})=>{
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



const onSubmit = async ()=>{
  book.get(form).then(({data})=>{
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
const onResetSubmit = async ()=>{
  form.title = "";
  form.author = [];
  form.release_time = "";
  form.price = "";
  form.isbn = '';
  await onSubmit()
}

const addSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      book.put({},addForm,{}).then(({data})=>{
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

const addBorrowSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      borrow.put({},addBorrow,{}).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        ElMessage.success("借书成功")
        dialogAddBorrowFormVisible.value = false;
      }).catch(err=>{
        ElMessage.error(err)
      })
    } else {
      ElMessage.error('error submit!')
      return false
    }
  })
}

const editSubmit = async (form)=>{
  form.validate((valid) => {
    if (valid) {
      book.post({},editForm,{}).then(({data})=>{
        if(data.code !== 200){
          ElMessage.error(data.msg)
          return
        }
        ElMessage.success("修改成功")
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

const filterMethod = (query, item) => {
  return item.name.toLowerCase().includes(query.toLowerCase())
}

const showBorrowDialog = (id) => {
  dialogAddBorrowFormVisible.value = true;
  addBorrow.book_id = id;
}

const addCopy = (id) => {
  book_copy.put({},{book_id:id}).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    ElMessage.success("添加成功")
  }).catch(err=>{
    ElMessage.error(err)
  })
}

onBeforeMount(()=>{
  onSubmit()
  author.get({page_size:10}).then(({data})=>{
    if(data.code !== 200){
      ElMessage.error(data.msg)
      return
    }
    authors.push(...data.data.infos);

  }).catch(err=>{
    ElMessage.error(err)
  })
})

const rule_date = (rule, value, callback)=>{
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
  title:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("标题没有填写"))
        }
        callback()
      },
    }
  ],
  isbn:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("isbn没有填写"))
        }
        callback()
      },
    }
  ],
  release_time:[
    {trigger: 'blur' ,
      validator:rule_date,
    }
  ],

})

const borrowRules = reactive({
  user_id:[
    {trigger: 'blur' ,
      validator(rule, value, callback){
        if(value === ''){
          callback(new Error("用户ID没有填写"))
        }
        callback()
      },
    },
  ],
  return_time:[
    {trigger: 'blur' ,
      validator:rule_date,
    }
  ],

})

</script>

<template>

  <el-dialog v-model="dialogFormVisible" title="Add Author">
    <el-form :rules="rules" ref="addFormRef" :model="addForm" label-width="100px">
      <el-form-item prop="title" label="标题">
        <el-input v-model="addForm.title" placeholder="Title" size="large"/>
      </el-form-item>
      <el-form-item prop="isbn" label="ISBN">
        <el-input v-model="addForm.isbn" placeholder="ISBN Code" size="large"/>
      </el-form-item>
      <el-form-item prop="author" label="作者">
        <el-transfer
            v-model="addForm.author"
            filterable
            :filter-method="filterMethod"
            filter-placeholder="State Abbreviations"
            :data="authors"
            :props="{
              key: 'id',
              label: 'name',
            }"
            :titles="['所有作者', '当前作者']"
        />
      </el-form-item>
      <el-form-item prop="price" label="price">
        <el-input-number v-model="addForm.price" placeholder="price" size="large"/>
      </el-form-item>
      <el-form-item prop="release_time" label="发布日期">
        <el-date-picker
            v-model="addForm.release_time"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
      </el-form-item>

    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogEditFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addSubmit(addFormRef)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog v-model="dialogEditFormVisible" :title="'Edit Book:'+editForm.title">
    <el-form :rules="rules" ref="editFormRef" :model="editForm" label-width="100px">
      <el-form-item prop="title" label="标题">
        <el-input v-model="editForm.title" placeholder="Title" size="large"/>
      </el-form-item>
      <el-form-item prop="isbn" label="ISBN">
        <el-input v-model="editForm.isbn" placeholder="ISBN Code" size="large"/>
      </el-form-item>
      <el-form-item prop="author" label="作者">
        <el-transfer
            v-model="editForm.author"
            filterable
            :filter-method="filterMethod"
            :props="{
              key: 'id',
              label: 'name',
            }"
            :right-default-checked="addForm.author"
            filter-placeholder="State Abbreviations"
            :data="authors"
            :titles="['所有作者', '当前作者']"
        />
      </el-form-item>
      <el-form-item prop="price" label="price">
        <el-input-number v-model="editForm.price" placeholder="price" size="large"/>
      </el-form-item>
      <el-form-item prop="birthday" label="发布日期">
        <el-date-picker
            v-model="editForm.release_time"
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


  <el-dialog v-model="dialogAddBorrowFormVisible" :title="'Borrow Book:'+addBorrow.book_id">
    <el-form :rules="borrowRules" ref="addBorrowRef" :model="addBorrow" label-width="100px">
      <el-form-item prop="user_id" label="用户id">
        <el-input-number :precision="0" v-model="addBorrow.user_id" placeholder="User Id" size="large"/>
      </el-form-item>

      <el-form-item prop="return_time" label="预计归还时间">
        <el-date-picker
            v-model="addBorrow.return_time"
            type="date"
            value-format="YYYY-MM-DD"
            size="large"
        />
      </el-form-item>

    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogEditFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addBorrowSubmit(addBorrowRef)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <div class="user-view">
    <el-form :inline="true" :model="form" class="demo-form-inline">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="Title" />
      </el-form-item>
      <el-form-item label="ISBN">
        <el-input v-model="form.isbn" placeholder="ISBN" />
      </el-form-item>
      <el-form-item label="发布日期范围">
        <el-date-picker
            v-model="release_time"
            type="daterange"
            range-separator="到"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="价格范围">
        <el-input-number v-model="price[0]" @change="changeMin" :min="0" :precision="2" :step="0.5"/>
        -
        <el-input-number v-model="price[1]" :min="price[0]" :precision="2" :step="0.5"/>
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
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="isbn" label="ISBN" />
      <el-table-column prop="price" label="价格" />
      <el-table-column prop="author" width="250px" label="作者" >
        <template #default="scope">
            <el-tag v-for="(item,index) in scope.row.author" :key="index">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="release_time" label="发布日期" />
      <el-table-column label="借书 / 添加副本">
        <template #default="scope">
          <el-button size="small" type="success" @click="showBorrowDialog(scope.row.id)" text>借书</el-button>
          <el-button size="small" type="primary" @click="addCopy(scope.row.id)" text>添加副本</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="dialogEditFormVisible = true ;handleEdit(scope.$index, scope.row)"
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