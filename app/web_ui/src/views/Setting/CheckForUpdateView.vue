<script setup lang="ts">
import AppPage from '@/components/common/AppPage.vue'
import { onMounted } from 'vue'
import { app_version, useUpdate } from '@/hooks/useUpdate'
const { updateState, update_update_store } = useUpdate()

onMounted(() => {
  update_update_store()
})
</script>
<template>
  <AppPage :sub_subtitle="`当前版本 ${app_version}`">
    <div
      v-if="updateState.update_loading"
      class="w-full min-h-[50vh] flex justify-center items-center"
    >
      <div class="loading loading-spinner loading-lg"></div>
    </div>
    <div
      v-else-if="updateState.update_result && updateState.update_result.has_update"
      class="text-lg font-medium"
    >
      有新版本更新
      <div class="text-gray-500 text-base">
        版本 {{ updateState.update_result.latest_version }} 已经发布.
      </div>
      <a
        :href="updateState.update_result.link"
        class="btn btn-neutral min-w-[180px] mt-6"
        target="_blank"
        >下载更新</a
      >
    </div>
    <div
      v-else-if="updateState.update_result && !updateState.update_result.has_update"
      class="text-lg font-medium"
    >
      没有新版本可用
      <div class="text-gray-500 text-base">你正在使用最新版软件</div>
    </div>
    <div v-else class="text-lg font-medium">
      更新检查失败
      <div class="text-error text-base">{{ updateState.update_error?.message }}</div>
    </div>
  </AppPage>
</template>
