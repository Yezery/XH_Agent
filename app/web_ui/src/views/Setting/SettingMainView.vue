<script setup lang="ts">
import AppPage from '@/components/common/AppPage.vue'
import { HeartIcon } from '@heroicons/vue/24/outline';
const sections = [
  {
    name: 'AI 模型',
    description: '选择并管理你的模型.',
    href: '/settings/providers',
    button_text: '进入设置',
  },
  {
    name: '软件更新',
    description: '检查是否有新版本的软件可用.',
    href: '/settings/check_for_update',
    button_text: '检查更新',
  },
  {
    name: '系统缓存',
    description: '清理系统缓存，以释放存储空间.',
    href: '/settings/system_cache',
    button_text: '进入清理',
  },
]
</script>
<template>
  <AppPage title="设置">
    <div class="flex flex-col gap-8 max-w-[700px] mt-8">
      <div
        v-for="section in sections"
        :key="section.name"
        class="flex flex-col md:flex-row gap-4 md:items-center"
      >
        <div class="grow">
          <h3 class="font-medium">{{ section.name }}</h3>
          <p class="text-sm text-gray-500">{{ section.description }}</p>
        </div>
        <RouterLink :to="section.href" class="btn btn-soft" style="min-width: 14rem">
          {{ section.button_text }}
        </RouterLink>
      </div>
      <div
        class="flex flex-col md:flex-row gap-4 md:items-center"
      >
        <div class="grow">
          <h3 class="font-medium"><HeartIcon class="size-5 inline-block"></HeartIcon> 支持</h3>
          <p class="text-sm text-gray-500">请他喝一杯咖啡吧！</p>
        </div>
        <a href="https://www.zivye.asia/zh/support" target="_blank" class="btn btn-soft" style="min-width: 14rem">
          来啦
        </a>
      </div>
    </div>
  </AppPage>
</template>
<style scoped></style>
