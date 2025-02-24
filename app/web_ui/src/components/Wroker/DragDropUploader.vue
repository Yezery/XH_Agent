<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { Vue3Lottie } from 'vue3-lottie'
import uploadAdd from '@/assets/uploadAdd.json'
import uploadOk from '@/assets/uploadOk.json'
const props = defineProps({
  modelValue: Boolean,
})
const isUpload = computed(() => props.modelValue)
const emit = defineEmits(['handleFileSelect'])
const dragging = ref(false)
const fileName = ref('')

function handleDrop(event: DragEvent) {
  event.preventDefault()
  dragging.value = false
  if (event.dataTransfer?.files?.length) {
    const file = event.dataTransfer.files[0] // 只取第一个文件
    fileName.value = file.name
    emit('handleFileSelect', file)
  }
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files?.length) {
    const file = target.files[0] // 只取第一个文件
    fileName.value = file.name
    emit('handleFileSelect', file)
  } else {
    fileName.value = ''
  }
  target.value = '' // 清空文件输入框
}
</script>

<template>
  <!--  -->
  <div
    :class="[
      isUpload
        ? 'border-gradient'
        : 'rounded-lg border-2 border-dashed transition-all hover:border-blue-500 hover:bg-gray-100',
      'rounded-xl',
    ]"
  >
    <div
      role="presentation"
      class="cursor-pointer padding-1 rounded-xl bg-white transition-all hover:bg-white/90"
      @dragover.prevent="dragging = true"
      @dragleave="dragging = false"
      @drop="handleDrop"
    >
      <input
        type="file"
        id="docFileInput"
        class="hidden"
        @change="handleFileSelect"
        accept=".docx"
      />
      <label
        for="docFileInput"
        class="flex h-full w-full cursor-pointer flex-col items-center justify-center p-6"
      >
        <template v-if="!isUpload">
          <!-- <DocumentPlusIcon class="size-6"></DocumentPlusIcon> -->
          <Vue3Lottie
            class="inline-block"
            :animation-data="uploadAdd"
            direction="alternate"
            height="1.8rem"
            width="1.8rem"
          />
          <p class="mt-2 text-gray-600">
            拖拽 <u>实验报告模版</u> 或
            <span class="text-blue-500">点击上传</span>
          </p>
        </template>
        <template v-else>
          <!-- <DocumentCheckIcon class="size-6">pi</DocumentCheckIcon> -->
          <Vue3Lottie
            class="inline-block"
            :animation-data="uploadOk"
            :loop="false"
            height="1.8rem"
            width="1.8rem"
          />
          <p class="mt-2 text-gray-600">{{ fileName }}</p>
        </template>
      </label>
    </div>
  </div>
</template>
<style scoped>
.border-gradient {
  z-index: 1;
  position: relative;
}

.border-gradient::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    #ff0000,
    #ff7300,
    #ffeb00,
    #47ff00,
    #00ffee,
    #2b65ff,
    #8000ff,
    #ff0080
  );
  border-radius: 15px;
  z-index: -1;
  animation: borderFlow 4s linear infinite;
}

@keyframes borderFlow {
  0% {
    filter: hue-rotate(0deg);
  }
  100% {
    filter: hue-rotate(360deg);
  }
}
</style>
