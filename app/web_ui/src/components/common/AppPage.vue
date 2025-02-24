<template>
  <div class="flex flex-row">
    <div class="flex flex-col grow">
      <h1 class="text-2xl font-bold">
        {{ title }}
      </h1>
      <p class="text-base font-medium mt-1">{{ prpos.subtitle }}</p>
      <!-- <p class="text-sm font-light mt-1">
        <a href="{sub_subtitle_link}" class="link" target="_blank"> </a>
      </p> -->
      <p class="text-sm font-light mt-1">{{ prpos.sub_subtitle }}</p>
    </div>
  </div>

  <div :class="no_y_padding ? '' : 'mt-8 mb-12'">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import router from '@/router'
import { computed, onMounted, ref } from 'vue'

const prpos = defineProps({
  subtitle: {
    type: String,
    required: false,
  },
  sub_subtitle: {
    type: String,
    required: false,
  },
  no_y_padding: {
    type: Boolean,
    default: false,
  },
  modelValue: String,
})
const title = computed(() => {
  if (prpos.modelValue) {
    return prpos.modelValue
  }
  return router.currentRoute.value.name
})
</script>
