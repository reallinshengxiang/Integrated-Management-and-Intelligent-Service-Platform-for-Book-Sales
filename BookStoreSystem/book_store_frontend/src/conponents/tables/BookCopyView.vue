<script setup>

import {reactive, watch, onBeforeMount, computed, ref} from "vue";
import {author, book_copy, user} from "../../api";
import {useRoute} from "vue-router";
import {ElMessage} from "element-plus";


const tableData = ref([])

const route = useRoute();

const form = reactive({
  page_size:10,
  page_num:1,
  title:"",
  is_borrow:null
})



const total = ref(1)


watch(form, (n,o)=>{
  route.query.page_num = n.page_num
})


const handleDelete = (index, row)=>{
  book_copy.delete({id:row.id}).then(({data})=>{
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
  form.title= "";

}

const onSubmit = async ()=>{
  book_copy.get(form).then(({data})=>{
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


onBeforeMount(()=>{
  onSubmit()
})

</script>

<template>

  <div class="user-view">
    <el-form :inline="true" :model="form" class="demo-form-inline">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="Title" />
      </el-form-item>
      <el-form-item  label="是否借出">
        <el-radio-group v-model="form.is_borrow" size="large">
          <el-radio-button label="是" />
          <el-radio-button label="否" />
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onResetSubmit">重置并查询</el-button>
      </el-form-item>

    </el-form>
    <el-table
        :data="tableData"
        style="width: 100%"
    >
      <el-table-column prop="id" label="id" />
      <el-table-column prop="book_id" label="书本Id" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="is_borrow" label="是否已经借出" style="" :formatter="(row, column, cellValue, index)=>{return cellValue ? '是' : '否'}" />
      <el-table-column label="操作">
        <template #default="scope">
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