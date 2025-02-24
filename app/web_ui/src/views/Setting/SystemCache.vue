<script setup lang="ts">
import AppPage from '@/components/common/AppPage.vue'
import system_api from '@/api/system_api'
import { onMounted, ref } from 'vue'
import { useMessage } from '@/hooks/useMessage'
import { ArchiveBoxIcon, BoltIcon } from '@heroicons/vue/24/outline'
const message = useMessage()

const total_size = ref('0 B')
const fileCount = ref(0)

onMounted(async () => {
  await getCacheInfo()
})

async function getCacheInfo() {
  const { data } = await system_api.getCacheInfo()
  fileCount.value = data.fileCount
  total_size.value = data.total_size
}

async function deleteCache() {
  if (await system_api.deleteCache()) {
    message['success']('清除成功', `释放了 ${total_size.value} 内存`)
    await getCacheInfo()
    // @ts-expect-error showModal is not a method on HTMLElement
    document.getElementById('cleanDialog')?.close()
  } else {
    message['error']('清除失败', '系统错误')
  }
}
</script>
<template>
  <AppPage :no_y_padding="true">
    <div class="stats mt-4">
      <div class="stat">
        <div class="stat-figure text-black">
          <BoltIcon class="inline-block h-8 w-8 stroke-current"></BoltIcon>
        </div>
        <div class="stat-title">内存占用</div>
        <div class="stat-value">{{ total_size }}</div>
        <div class="stat-desc">文件数量 {{ fileCount }} 个</div>
      </div>
    </div>
    <div class="mt-4">
      <button class="btn btn-link text-black" onclick="cleanDialog.showModal()">清除</button>
    </div>

    <dialog id="cleanDialog" class="modal">
      <div class="modal-box">
        <h3 class="text-lg font-bold">清除缓存</h3>
        <p class="py-4">这将释放 {{ total_size }} 内存</p>
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>

        <div class="modal-action">
          <button class="btn" @click="deleteCache">确认</button>
        </div>
      </div>
    </dialog>
  </AppPage>
</template>
