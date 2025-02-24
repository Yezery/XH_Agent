<script setup lang="ts">
import { ref, defineProps, watch } from 'vue'
import {
  TrashIcon,
  PhotoIcon,
  PencilIcon,
  PlusIcon,
  SparklesIcon,
  CodeBracketIcon,
  ArrowUturnLeftIcon
} from '@heroicons/vue/24/outline'
import work_api from '@/api/work_api'
import { useMessage } from '@/hooks/useMessage';
const message = useMessage()
const props = defineProps<{
  image_path: string
  _id: string
  model?: string
  provider?: string
}>()

const emit = defineEmits(['delete', 'edit', 'insertText', 'insertImage'])
function onDelete() {
  emit('delete', props._id)
}
const script_text = ref('')
const old_text = ref('')
watch(script_text, (newVal) => {
  emit('edit', newVal)
  if (script_text.value.length > 30) {
    show_text.value = script_text.value.slice(0, 20) + '...'
  } else if (script_text.value.length == 0) {
    show_text.value = '请输入描述'
  }else {
    show_text.value = script_text.value
  }
})

const show_text = ref('请输入描述')
const add_T = ref(false)
const rewriteFinish = ref(true)
function insertText() {
  emit('insertText', props._id)
}
function handInsertImageFile(event: Event) {
  const target = event.target as HTMLInputElement
  if (!target.files) {
    return
  }
  for (const file of target.files) {
    emit('insertImage', props._id, file)
  }
}
function insertImage() {
  document.getElementById('insertImage')?.click()
}

// function aiRewrite(){
//   emit('aiRewrite', _id)
// }
async function aiRewrite() {
  if (props.model != '' && props.provider != '' && script_text.value != '') {
    rewriteFinish.value = false
    try {
      let buffer: string = ''
      old_text.value = script_text.value
      const stream = await work_api.rewrite({
        model: props.model,
        provider: props.provider,
        message: script_text.value,
      })
      const reader = stream.getReader()
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += value
        script_text.value = buffer
      }
    } catch (error) {
      message['error']('发生错误','重写失败！')
      old_text.value = script_text.value
    } finally {
      rewriteFinish.value = true
    }
  }
}
</script>

<template>
  <div class="w-full">
    <div
      @mouseenter="add_T = true"
      @mouseleave="add_T = false"
      class="pt-2 pb-2  w-full flex justify-center items-center"
    >
      <Transition>
        <div v-if="add_T" class="grid grid-cols-3 gap-10">
          <button
            @click="insertText"
            class="btn outline-1 bg-white rounded-xl h-[36px] -outline-offset-1 flex justify-center items-center cursor-pointer"
          >
            <PlusIcon class="size-5"></PlusIcon>
            纯文本
          </button>
          <button
            @click="insertImage"
            class="btn outline-1 bg-white rounded-xl h-[36px] -outline-offset-1 flex justify-center items-center cursor-pointer"
          >
            <PlusIcon class="size-5"></PlusIcon>
            <input
              type="file"
              id="insertImage"
              class="hidden h-full"
              @change="handInsertImageFile"
              accept="image/jpeg, image/png"
              multiple
            />
            插入图片
          </button>
          <button
            type="button"
            @click="onDelete"
           class="btn outline-1  rounded-xl h-[36px]  -outline-offset-1 flex justify-center items-center cursor-pointer hover:bg-red-400/70 hover:text-white hover:outline-white"
          >
          <TrashIcon class="size-4"></TrashIcon>
          删除下项
          </button>
        </div>
      </Transition>
    </div>
    <div class="collapse collapse-arrow bg-base-100 border border-base-300">
      <input type="checkbox" />
      <!-- <input type="radio" name="my-accordion-1" :checked="false" /> -->
      <div class="collapse-title font-semibold flex justify-between items-center">
        <div>{{ show_text }}</div>
        <div class="flex justify-center items-end">
          <PhotoIcon v-if="image_path != ''" class="size-6 ml-3 mr-3"></PhotoIcon>
          <PencilIcon v-if="script_text.length > 0" class="size-6 ml-3"></PencilIcon>
        </div>
      </div>
      <div class="collapse-content text-sm">
        <div class="bg-base-100 mb-3 pl-2.5 pr-2.5">
          <img
            v-if="image_path != ''"
            class="aspect-auto rounded-xl object-cover"
            :src="image_path"
            alt=""
          />
          <div class="items-start mt-1.5">
            <form action="#" class="relative">
              <div
                class="rounded-lg bg-white outline-1 -outline-offset-1 outline-gray-100 focus-within:outline-1 focus-within:-outline-offset-2 focus-within:outline-black"
              >
                <textarea
                  rows="4"
                  v-model="script_text"
                  :disabled="!rewriteFinish"
                  name="comment"
                  id="comment"
                  class="border-0 block w-full resize-none bg-transparent px-3 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="编辑描述内容"
                />

                <!-- Spacer element to match the height of the toolbar -->
                <div class="py-2" aria-hidden="true">
                  <!-- Matches height of button in toolbar (1px border + 36px content height) -->
                  <div class="py-px">
                    <div class="h-9" />
                  </div>
                </div>
              </div>

              <div class="absolute inset-x-0 bottom-0 flex justify-between py-2 pr-2 pl-3">
                <div class="flex items-center justify-between space-x-5 w-full">
                  <div class="flex items-center space-x-5">
                    <div class="flex items-center">
                      <div class="tooltip tooltip-bottom" data-tip="Ai 重写">
                        <button
                          type="button"
                          @click="aiRewrite"
                          :disabled="!rewriteFinish || (props.model == '' && script_text == '')"
                          :class="[
                            ' -m-2.5 flex size-10 items-center justify-center rounded-full text-black',
                            !rewriteFinish || props.model == '' || script_text == ''
                              ? 'cursor-not-allowed'
                              : 'hover:text-indigo-600 cursor-pointer',
                          ]"
                        >
                          <SparklesIcon class="size-5"></SparklesIcon>
                          <span class="sr-only">ai rewrite</span>
                        </button>
                      </div>
                    </div>
                    <div class="flex items-center">
                      <div class="tooltip tooltip-bottom" data-tip="格式化描述">
                        <button
                          type="button"
                          @click="
                            () => {
                              script_text = script_text
                                .replace(/<think>.*?<\/think>/gs, '')
                                .replace(/\n{2,}/g, '\n')
                                .trim()
                            }
                          "
                          class="cursor-pointer -m-2.5 flex size-10 items-center justify-center rounded-full text-black"
                        >
                          <CodeBracketIcon class="size-5" />
                          <span class="sr-only">format </span>
                        </button>
                      </div>
                    </div>
                    <div class="flex items-center">
                      <div class="tooltip tooltip-bottom" data-tip="撤回修改">
                        <button
                          :disabled="!rewriteFinish || old_text == '' || old_text == script_text"
                          type="button"
                          @click="
                            () => {
                              script_text = (old_text == '' ? script_text:old_text)
                            }
                          "
                          class="cursor-pointer -m-2.5 flex size-10 items-center justify-center rounded-full text-black"
                        >
                          <ArrowUturnLeftIcon class="size-5" />
                          <span class="sr-only">撤回修改</span>
                        </button>
                      </div>
                    </div>

                  </div>
                  <div class="flex items-center"></div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
