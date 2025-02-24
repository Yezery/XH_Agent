<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import {
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from '@heroicons/vue/24/outline'
import { XMarkIcon } from '@heroicons/vue/20/solid'

// 消息类型
type MessageType = 'info' | 'success' | 'warning' | 'error'

// 消息对象
interface MessageItem {
  id: number
  title: string
  content: string
  type: MessageType
}

// 消息队列
const messages = reactive<MessageItem[]>([])

// 显示消息
const addMessage = (
  title: string,
  content: string,
  type: MessageType = 'info',
  duration = 3000,
) => {
  const id = Date.now()
  messages.push({ id, title, content, type })

  // 自动销毁
  setTimeout(() => {
    removeMessage(id)
  }, duration)
}

// 删除消息
const removeMessage = (id: number) => {
  const index = messages.findIndex((msg) => msg.id === id)
  if (index !== -1) messages.splice(index, 1)
}

// 颜色样式
const typeClass = computed(() => ({
  info: 'text-green-400',
  success: 'text-green-400',
  warning: 'text-yellow-400',
  error: 'text-red-400',
}))

// 图标映射
const icons = {
  info: InformationCircleIcon,
  success: CheckCircleIcon,
  warning: ExclamationTriangleIcon,
  error: XCircleIcon,
}

// 让外部可以调用
defineExpose({ addMessage })
</script>

<template>
  <Teleport to="html">
    <div
      aria-live="assertive"
      class="pointer-events-none fixed inset-0 right-1.5 top-4.5  flex items-end px-4 py-6 sm:items-start sm:p-6"
    >
      <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
        <transition-group
          enter-active-class="transform ease-out duration-300 transition"
          enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
          enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="z-1000 pointer-events-auto w-full  max-w-sm overflow-hidden rounded-2xl bg-white ring-1 shadow-md ring-black/5"
            :class="typeClass[msg.type]"
          >
            <div class="p-4 flex items-start">
              <component
                :is="icons[msg.type]"
                class="size-6 flex-shrink-0"
                :class="typeClass[msg.type]"
                aria-hidden="true"
              />
              <div class="ml-3 w-0 flex-1">
                <p class="text-sm font-medium text-black">{{ msg.title }}</p>
                <p class="mt-1 text-sm text-black">{{ msg.content }}</p>
              </div>
              <div class="ml-4 flex shrink-0">
                <div
                  type="button"
                  @click="removeMessage(msg.id)"
                  class="cursor-pointer inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="size-5" aria-hidden="true" />
                </div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
p {
  word-break: break-word;
}
</style>
