<script setup lang="ts">
import AppPage from '@/components/common/AppPage.vue'
import { nextTick, onMounted, ref, watch, type Ref } from 'vue'
import { ArrowPathIcon, PlusIcon } from '@heroicons/vue/24/outline'
import work_api from '@/api/work_api'
import ImageGroup from '@/components/Wroker/ImageGroup.vue'
import DragDropUploader from '@/components/Wroker/DragDropUploader.vue'
import provider_api from '@/api/provider_api'
import { ChevronUpDownIcon } from '@heroicons/vue/16/solid'
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue'
import { CheckIcon, CodeBracketIcon } from '@heroicons/vue/20/solid'
import { Vue3Lottie } from 'vue3-lottie'
import picture from '@/assets/picture.json'
import refresh_Lottie from '@/assets/refresh.json'
import { useMessage } from '@/hooks/useMessage'
const message = useMessage()
type ImageGroupType = {
  _id: string
  url: string
  text: string
  file: File
}
const imageGroup = ref(new Map<string, ImageGroupType>())
const dropArea = ref<HTMLDivElement>()
const summaryEl = ref<HTMLTextAreaElement | null>()
const isUpload = ref(false)
const activeModels = ref<{ model: string; provider: string }[]>([])
const form = ref({
  name: '',
  _id: '',
  course: '',
  fileName: '',
  file: new File([], ''),
})
const summry = ref('')
const pageTitle = ref('等待上传实验报告模版...')
const add_B = ref(false)
const gen_btn_disable_status = ref(false)
const model_select_disable_status = ref(false)
function updateUI(status: boolean) {
  if (status) {
    gen_btn_disable_status.value = true
    model_select_disable_status.value = true
    if (summaryEl.value) {
      summaryEl.value.placeholder = '正在生成中，请稍后...'
    }
  } else {
    gen_btn_disable_status.value = false
    model_select_disable_status.value = false
    if (summaryEl.value) {
      summaryEl.value.placeholder = '请选择模型再点击生成 或 直接编辑'
    }
  }
}
async function scrollToBottom(HtmlElement: HTMLElement) {
  await nextTick() // 确保 DOM 更新完成

  requestAnimationFrame(() => {
    setTimeout(() => {
      HtmlElement.scrollTo({
        top: HtmlElement.scrollHeight,
        behavior: 'smooth', // 平滑滚动
      })
    }, 50)
  })
}

type selectedModelType = {
  model: string
  provider: string
}
const selectedModel: Ref<selectedModelType> = ref({
  model: '',
  provider: '',
})

async function handleDocxFile(file: File) {
  await checkDocx(file)
}
async function removeGroup(id: string) {
  imageGroup.value.delete(id)
  imageGroup.value = new Map(imageGroup.value) // 触发更新
}

let lastId = Date.now() // 维护全局唯一 ID 递增
async function handleFile(target: HTMLInputElement | DataTransfer) {
  const formData = new FormData()
  if (target?.files) {
    for (const file of target.files) {
      const id = (++lastId).toString() // 生成唯一字符串 ID
      imageGroup.value.set(id, {
        _id: id,
        text: '',
        url: URL.createObjectURL(file),
        file: file,
      })
      imageGroup.value = new Map(imageGroup.value)
      formData.append('files', file)
    }
    if (target instanceof HTMLInputElement) {
      target.value = ''
    }
    await work_api.image_upload(formData)
  }
  scrollToBottom(dropArea.value as HTMLDivElement)
}

async function handleFileDrop(event: DragEvent) {
  event.preventDefault()
  event.stopPropagation()
  const target = event.dataTransfer as DataTransfer
  await handleFile(target)
}

async function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  await handleFile(target)
}

function insertText(id: string) {
  if (!imageGroup.value.has(id)) {
    console.error(`Key '${id}' not found.`)
    return
  }
  const newMap = new Map<string, ImageGroupType>() // 新的 Map
  const newKey = (++lastId).toString() // 生成新的唯一键
  const newImageGroupType: ImageGroupType = {
    _id: newKey,
    url: '',
    text: '',
    file: new File([], ''),
  }
  for (const [key, value] of imageGroup.value) {
    if (key === id) {
      newMap.set(newKey, newImageGroupType) // 先插入新值
    }
    newMap.set(key, value) // 再插入原来的值
  }
  imageGroup.value = newMap // 触发 Vue 响应式
}

async function insertImage(id: string, file: File) {
  if (!imageGroup.value.has(id)) {
    console.error(`Key '${id}' not found.`)
    return
  }
  const newMap = new Map<string, ImageGroupType>() // 新的 Map
  const newKey = (++lastId).toString() // 生成新的唯一键
  const newImageGroupType: ImageGroupType = {
    _id: newKey,
    url: URL.createObjectURL(file),
    text: '',
    file: file,
  }
  for (const [key, value] of imageGroup.value) {
    if (key === id) {
      newMap.set(newKey, newImageGroupType) // 先插入新值
    }
    newMap.set(key, value) // 再插入原来的值
  }
  imageGroup.value = newMap // 触发 Vue 响应式
  const formData = new FormData()
  formData.append('files', file)
  await work_api.image_upload(formData)
}

function triggerFileInput() {
  document.getElementById('fileInput')?.click()
}
function triggerTextInput() {
  const newKey = (++lastId).toString()
  const newImageGroupType: ImageGroupType = {
    _id: newKey,
    url: '',
    text: '',
    file: new File([], ''),
  }
  imageGroup.value.set(newKey, newImageGroupType) // 先插入新值
}

async function checkDocx(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await work_api.docx_upload(formData)
  if (data) {
    isUpload.value = true
    form.value.file = file
    form.value.fileName = file.name.split('.')[0]
    message['success']('成功', '上传成功')
    return
  }
  isUpload.value = false
  form.value.fileName = ''
  message['error']('失败', '文件不符合要求')
}
async function genSummary() {
  summry.value = ''
  updateUI(true)
  try {
    const stream = await work_api
      .gen_summary({
        model: selectedModel.value.model,
        provider: selectedModel.value.provider,
        message: '',
      })

    const reader = stream.getReader()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      summry.value += value
      scrollToBottom(summaryEl.value as HTMLTextAreaElement)
    }
    updateUI(false)
  } catch (error) {
    console.log(error)

    updateUI(false)
  }
}

async function getModelList() {
  const { data } = await provider_api.availableModels()
  Object.keys(data).forEach((key) => {
    data[key].forEach((modelName: string) => {
      activeModels.value.push({
        model: modelName,
        provider: key,
      })
    })
  })
}

async function loadUserInfo() {
  const { data } = await work_api.loadUserInfo()

  form.value.name = data.name == null ? '' : data.name
  form.value._id = data.id == null ? '' : data.id
  form.value.course = data.course == null ? '' : data.course
}

async function submit() {
  const images_texts: { text: string; imageName: string }[] = []
  imageGroup.value.forEach((item) => {
    images_texts.push({
      text: item.text,
      imageName: item.file.name,
    })
  })

  const response = await work_api.work_run({
    name: form.value.name,
    id: form.value._id,
    course: form.value.course,
    docxName: form.value.fileName,
    summary: summry.value,
    images_texts: images_texts,
  })
  const blob = new Blob([response.data], {
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `${form.value.course}_${form.value.name}_${form.value._id}_${form.value.fileName}.docx`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
async function refresh_model() {
  activeModels.value = []
  await provider_api.ollamaConnect('')
  await getModelList()
  if (modelSelect.value) {
    modelSelect.value?.$el.click()
  }
}

const modelImageMap: Record<string, string> = {
  ollama: '/images/ollama.svg',
  deepseek: '/images/deepseek.svg',
  openAi: '/images/openai.svg',
  qwen: '/images/qwen.svg',
  siliconflow: '/images/siliconflow.svg',
  moonshot: 'images/moonshot.svg',
  hunyuan:'/images/hunyuan.svg'
}

const modelSelect = ref()
const aiRewriteSign = ref(false)
onMounted(async () => {
  await provider_api.apiKeyProviderStatus()
  await getModelList()
  await loadUserInfo()
})

watch(
  form.value,
  (n) => {
    if (form.value.fileName != '') {
      pageTitle.value = `${form.value._id}_${form.value.name}_${form.value.course}_${form.value.fileName}`
    }
  },
  {
    deep: true,
  },
)
</script>
<template>
  <AppPage v-model="pageTitle" :no_y_padding="true">
    <div class="mt-4 grid grid-cols-4">
      <div class="col-span-2 h-full w-full">
        <fieldset class="fieldset pr-8">
          <legend class="fieldset-legend"></legend>
          <DragDropUploader v-model="isUpload" @handle-file-select="handleDocxFile" />

          <legend class="fieldset-legend justify-start items-center mt-1">Ai 心得</legend>
          <div class="tooltip" :data-tip="selectedModel.model ? selectedModel.model : '未选择模型'">
          <div class="flex">
            <Listbox
              as="div"
              class="w-77"
              v-model="selectedModel"
              :disabled="model_select_disable_status"
            >
              <div class="relative mt-1">
                <ListboxButton
                  ref="modelSelect"
                  class="grid w-full cursor-default grid-cols-1 rounded-lg bg-white py-1.5 pr-2 pl-3 text-left text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-black sm:text-sm/6"
                >
                  <span class="col-start-1 row-start-1 flex items-center gap-3 pr-6">
                    <img
                      v-if="selectedModel.model != ''"
                      :src="modelImageMap[selectedModel.provider]"
                      :alt="selectedModel.provider"
                      class="size-5 shrink-0 rounded-full"
                    />
                    <span class="block truncate">{{ selectedModel.model }}</span>
                    <span v-if="selectedModel.model == ''" class="block truncate">未选择模型</span>
                  </span>
                  <ChevronUpDownIcon
                    class="col-start-1 row-start-1 size-5 self-center justify-self-end text-gray-500 sm:size-4"
                    aria-hidden="true"
                  />
                </ListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions
                    class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base ring-1 shadow-lg ring-black/5 focus:outline-hidden sm:text-sm"
                  >
                    <ListboxOption
                      as="template"
                      v-for="model in activeModels"
                      :key="model.model"
                      :value="model"
                      v-slot="{ active, selected }"
                    >
                      <li
                        :class="[
                          active ? ' bg-base-300 text-gray-900 outline-hidden' : 'text-gray-900',
                          'relative cursor-default py-2 pr-9 pl-3 select-none',
                        ]"
                      >
                        <div class="flex items-center">
                          <img
                            :src="modelImageMap[model.provider]"
                            :alt="model.provider"
                            class="size-5 shrink-0 rounded-full"
                          />
                          <span
                            :class="[
                              selected ? 'font-semibold' : 'font-normal',
                              'ml-3 block truncate',
                            ]"
                            >{{ model.model }}</span
                          >
                        </div>

                        <span
                          v-if="selected"
                          :class="[
                            active ? 'text-white' : 'text-black',
                            'absolute inset-y-0 right-0 flex items-center pr-4',
                          ]"
                        >
                          <CheckIcon class="size-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
            <button
              aria-label="刷新模型"
              :disabled="model_select_disable_status"
              @click="refresh_model"
              class="cursor-pointer ml-1 flex justify-center items-center"
            >
              <Vue3Lottie
                :animation-data="refresh_Lottie"
                :play-on-hover="true"
                width="2rem"
                height="2rem"
              ></Vue3Lottie>
            </button>
          </div>
        </div>
          <div class="flex items-start space-x-4">
            <div class="min-w-0 flex-1">
              <form action="#" class="relative">
                <div
                  class="rounded-lg bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-black"
                >
                  <textarea
                    ref="summaryEl"
                    rows="9"
                    name="comment"
                    v-model="summry"
                    placeholder="在此修改或编辑 AI 总结的内容 ✦"
                    id="comment"
                    class="border-0 block w-full resize-none bg-transparent px-3 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  />
                  <!-- Spacer element to match the height of the toolbar -->
                  <div class="py-2" aria-hidden="true">
                    <!-- Matches height of button in toolbar (1px border + 36px content height) -->
                    <div class="py-px">
                      <div class="h-9"></div>
                    </div>
                  </div>
                </div>

                <div class="absolute inset-x-0 bottom-0 flex justify-between py-2 pr-2 pl-3">
                  <div class="flex items-center space-x-5">
                    <div class="flex items-center">
                      <button
                        type="button"
                        @click="
                          () => {
                            summry = summry
                              .replace(/<think>.*?<\/think>/gs, '')
                              .replace(/\n{2,}/g, '\n')
                              .trim()
                          }
                        "
                        class="cursor-pointer"
                      >
                        <CodeBracketIcon class="size-5" aria-hidden="true" />
                        <span class="sr-only">format summary</span>
                      </button>
                    </div>
                  </div>
                  <div class="shrink-0">
                    <button
                      @click="genSummary"
                      :disabled="
                        !isUpload ||
                        activeModels.length == 0 ||
                        selectedModel.model == '' ||
                        gen_btn_disable_status
                      "
                      class="inline-flex items-center rounded-md btn btn-neutral text-sm font-semibold text-white shadow-xs"
                    >
                      <span v-if="!gen_btn_disable_status">生成</span>
                      <span v-else class="loading loading-spinner"></span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <legend class="fieldset-legend mt-1">文件命名格式</legend>
          <div class="mt-2 grid grid-cols-3">
            <div class="-mb-px -mr-px">
              <input
                type="text"
                class="block w-full rounded-tl-lg bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-black sm:text-sm/6"
                v-model="form.course"
                required
                placeholder="班级"
              />
            </div>
            <div class="-mb-px">
              <input
                type="text"
                class="block w-full bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-black sm:text-sm/6"
                v-model="form.name"
                required
                placeholder="姓名"
              />
            </div>
            <div class="-mb-px -ml-px">
              <input
                type="text"
                class="block w-full rounded-tr-lg bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-black sm:text-sm/6"
                v-model="form._id"
                required
                placeholder="学号"
              />
            </div>
            <div class="col-span-3">
              <input
                type="text"
                v-model="form.fileName"
                required
                placeholder="实验报告命名"
                class="block w-full rounded-b-lg bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-black sm:text-sm/6"
              />
            </div>
          </div>
          <div class="mt-4 grid grid-cols-1 gap-2">
            <button :disabled="!isUpload" class="btn rounded-lg btn-neutral" @click="submit">
              运 行
            </button>
          </div>
        </fieldset>
      </div>

      <!-- 实验报告图片展示 -->

      <div
        ref="dropArea"
        @drop="handleFileDrop"
        @dragover="
          (event) => {
            event.preventDefault()
          }
        "
        :class="[
          Array.from(imageGroup).length == 0
            ? 'col-span-2 flex mt-3  h-full w-full cursor-pointer justify-center rounded-lg border-2 border-dashed transition-all hover:border-blue-500 hover:bg-gray-100'
            : 'col-span-2 flex h-[45rem] w-full flex-col items-center overflow-y-scroll',
        ]"
      >
        <input
          type="file"
          id="fileInput"
          class="hidden h-full"
          @change="handleFileSelect"
          accept="image/jpeg, image/png"
          multiple
        />
        <label
          v-if="Array.from(imageGroup).length == 0"
          for="fileInput"
          class="flex h-full w-full cursor-pointer flex-col items-center justify-center"
        >
          <Vue3Lottie
            class="inline-block"
            :animation-data="picture"
            height="4rem"
            width="4rem"
            :speed="0.6"
          />
          <p class="mt-3 text-sm text-gray-600">
            拖拽 <u>描述图片</u> 或 <span class="text-sm text-blue-500">点击上传</span>
          </p>
        </label>
        <template v-if="Array.from(imageGroup).length > 0">
          <template v-for="item in Array.from(imageGroup.values())" :key="item._id">
            <Transition>
              <ImageGroup
                :image_path="item.url"
                v-model:model="selectedModel.model"
                v-model:provider="selectedModel.provider"
                :_id="item._id"
                @edit="
                  (text) => {
                    imageGroup.set(item._id, { ...item, text })
                  }
                "
                @delete="
                  (_id) => {
                    removeGroup(_id)
                  }
                "
                @insert-text="
                  (id) => {
                    insertText(id)
                  }
                "
                @insert-image="
                  (id, file) => {
                    insertImage(id, file)
                  }
                "
              />
            </Transition>
          </template>
          <div
            @mouseenter="add_B = true"
            @mouseleave="add_B = false"
            class="pt-0.5 pb-0.5 mb-2 mt-2 w-full flex justify-center items-center"
          >
            <div v-if="add_B" class="grid grid-cols-2 gap-10">
              <button
                class="btn outline-1 bg-white rounded-xl h-[36px] -outline-offset-1 flex justify-center items-center cursor-pointer"
                @click="triggerTextInput"
              >
                <PlusIcon class="size-5"></PlusIcon>
                纯文本
              </button>
              <button
                class="btn outline-1 bg-white rounded-xl h-[36px] -outline-offset-1 flex justify-center items-center cursor-pointer"
                @click="triggerFileInput"
              >
                <PlusIcon class="size-5"></PlusIcon>
                插入图片
              </button>
              <!-- <button class="btn btn-neutral cursor-pointer">纯文字</button>
              <button class="btn btn-neutral cursor-pointer">插入图片</button> -->
            </div>
            <div v-else>
              <div class="inline-grid *:[grid-area:1/1]">
                <div class="status status-accent animate-ping"></div>
                <div class="status status-accent"></div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </AppPage>
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
