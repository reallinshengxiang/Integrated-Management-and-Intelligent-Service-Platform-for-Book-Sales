<script setup>

import {ref, unref} from "vue";
import {ElMessage} from "element-plus";
import useClipboard from 'vue-clipboard3'
const popoverRef = ref()
const { toClipboard } = useClipboard()
const hide = (popover) => {
  unref(popover).hide()
}


const copy_url = async () => {

  try {
    await toClipboard(location.href)
    ElMessage.success("复制链接成功");
  } catch (e) {
    ElMessage.error("复制失败！");
  }
}

const email_url = 'mailto:?subject=提示管理系统！&body='+location.href

</script>

<template>
  <div class="footer">
      <div>@2025 . Integrated Management and Intelligent Service Platform for Book Sales</div>
      <el-popover ref="popoverRef" placement="top" :width="400" trigger="hover" >
        <template #reference>
          <el-button style="margin-right: 16px" type="primary" text>Share</el-button>
        </template>
        <el-row :span="8">
          <el-button type="info" @click="copy_url()" >复制链接</el-button>
          <a class="el-button el-button--success" :href="email_url" target="_blank">
            <span>根据邮件分享</span>
          </a>
          <el-button type="warning" @click="hide(popoverRef)" >取消</el-button>
        </el-row>
      </el-popover>
  </div>
</template>

<style lang="scss" scoped>

.footer{
  @include footer();
  width: 80%;
  height: 100%;
  padding: 0 10%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.link{

}

</style>