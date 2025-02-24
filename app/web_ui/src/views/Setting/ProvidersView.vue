<script setup lang="ts">
import AppPage from '@/components/common/AppPage.vue'
import { onMounted, ref, type Ref } from 'vue'
import provider_api from '@/api/provider_api'
import { CheckCircleIcon } from '@heroicons/vue/24/outline'
import { useMessage } from '@/hooks/useMessage'
const message = useMessage()
type Provider = {
  name: string
  id: string
  description: string
  image: string
  featured: boolean
  base_url: string
  provider_url: string
  free: boolean
}

type ProviderStatus = {
  connected: boolean
  error: string | null
  custom_description: string | null
  connecting: boolean
}
const status: Ref<{ [key: string]: ProviderStatus }> = ref({
  ollama: {
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  deepseek: {
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  openAi: {
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  qwen: {
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  siliconflow:{
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  moonshot:{
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  },
  hunyuan:{
    connected: false,
    connecting: false,
    error: null,
    custom_description: null,
  }
})
const provider = {
  id: 'ollama',
  name: 'Ollama',
  image: '/images/ollama.svg',
  description: '本地运行模型，无需API密钥',
  provider_url: 'https://ollama.com',
  featured: true,
}
const api_key_providers: Provider[] = [
{
    id: 'siliconflow',
    name: 'Siliconflow',
    image: '/images/siliconflow.svg',
    base_url: 'https://api.siliconflow.cn/v1',
    provider_url: 'https://cloud.siliconflow.cn/account/ak',
    description: '硅基流动平台',
    featured: true,
    free: true,
  },
  {
    id: 'hunyuan',
    name: 'Hunyuan',
    image: '/images/hunyuan.svg',
    base_url: 'https://api.hunyuan.cloud.tencent.com/v1',
    provider_url: 'https://console.cloud.tencent.com/hunyuan/api-key',
    description: '腾讯混元大模型',
    featured: false,
    free: true,
  },
  {
    id: 'moonshot',
    name: 'Moonshot',
    image: '/images/moonshot.svg',
    base_url: 'https://api.moonshot.cn/v1',
    provider_url: 'https://platform.moonshot.cn/console/api-keys',
    description: '月之暗面 Kimi',
    featured: false,
    free: true,
  },
{
    id: 'qwen',
    name: 'Qwen',
    image: '/images/qwen.svg',
    base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    provider_url: 'https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen',
    description: '通义千问',
    featured: false,
    free: true,
  },
  {
    id: 'deepseek',
    name: 'Deepseek',
    image: '/images/deepseek.svg',
    base_url: 'https://api.deepseek.com',
    provider_url: 'https://platform.deepseek.com/api_keys',
    description: '深度求索',
    featured: false,
    free: false,
  },
  {
    id: 'openAi',
    name: 'Chatanywhere',
    image: '/images/openai.svg',
    base_url: 'https://api.chatanywhere.tech/v1',
    provider_url: 'https://chatanywhere.apifox.cn/',
    description: '国内 OpenAI 镜像',
    featured: false,
    free: false,
  },


]

const current_provider: Ref<Provider> = ref({
  name: '',
  id: '',
  description: '',
  image: '',
  featured: false,
  base_url: '',
  provider_url: '',
  free: false,
})
function show_custom_ollama_url_dialog() {
  // @ts-expect-error showModal is not a method on HTMLElement
  document.getElementById('ollama_dialog')?.showModal()
}
const input_api_key = ref('')
const custom_ollama_url = ref('')
const loading_initial_providers = ref(true)
const initial_load_failure = ref(false)
const check_ollama_status = async () => {
  try {
    const res = await fetch('http://localhost:8757/api/settings')
    const data = await res.json()
    if (data['ollama_base_url']) {
      custom_ollama_url.value = data['ollama_base_url']
    }
  } catch (e) {
    console.error('check_ollama_status error', e)
  } finally {
  }
}
const connect_ollama = async (user_initated: boolean = true) => {
  status.value.ollama.connected = false
  status.value.ollama.connecting = user_initated
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let data: any = null
  try {
    data = await provider_api.ollamaConnect(custom_ollama_url.value)
    data = data.data
  } catch (error) {
    status.value.ollama.error = '连接失败请确保 Ollama 软件正在运行'
    status.value.ollama.connected = false
    status.value.ollama.connecting = false
    status.value.ollama.custom_description=provider.description
    return
  }

  if (data.models.length === 0) {
    status.value.ollama.error =
      "Ollama 正在运行，但没有可用的模型。可以使用 ollama cli 安装（例如 'ollama run deepseek-r1:1.5b')"
    return
  }
  status.value.ollama.error = null
  status.value.ollama.connected = true

  const supported_models_str =
    data.models.length > 0
      ? '以下支持的型号可用： ' + data.models.join(', ') + '. '
      : 'Ollama 没有可用的模型。'

  const custom_url_str =
    custom_ollama_url.value && custom_ollama_url.value == 'http://localhost:11434'
      ? ''
      : '自定义 Ollama URL: ' + custom_ollama_url.value

  const custom_url_show = custom_ollama_url.value == ''?'' : custom_url_str

  status.value.ollama.custom_description =
    'Ollama 连接成功. ' + supported_models_str + custom_url_show
}

const check_api_key_providers = async () => {
  loading_initial_providers.value = true
  const { data } = await provider_api.apiKeyProviderStatus()
  Object.keys(status.value).forEach((key) => {
    status.value[key].connecting = true
  })
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data.data.forEach((item: any) => {
    status.value[item.provider].connected = item.status
    status.value[item.provider].custom_description = item.message
  })
  loading_initial_providers.value = false
}

const connect_api_key_providers = async () => {
  await provider_api
    .apiKeyProviderConnect({
      api_key: input_api_key.value,
      base_url: current_provider.value.base_url,
      provider_name: current_provider.value.id,
    })
    .then((res) => {
      status.value[current_provider.value.id].connected = res.data.status
      if (res.data.status){
        message['success'](`连接 ${current_provider.value.id}`,"连接成功")
        // @ts-expect-error showModal is not a method on HTMLElement
        document.getElementById('api_modal')?.close()
      }else{
        message['error'](`连接 ${current_provider.value.id}`,"连接失败")
      }
    })
    .catch((e) => {
      status.value[current_provider.value.id].connected = false
      message['error'](`连接 ${current_provider.value.id}`,"连接失败（请检查 API Key）")
    })
}
const disconnect_provider = async (provider: string) => {
  if (!confirm('你确定要断开连接吗？')) {
    return
  }
  if (await provider_api.disconnect(provider)) {
    status.value[provider].connected = false
  }
}

function opendialog(provider: Provider) {
  // @ts-expect-error showModal is not a method on HTMLElement
  document.getElementById('api_modal')?.showModal()
  current_provider.value = provider
}
onMounted(async () => {
  await check_ollama_status()
  await connect_ollama(false).then((re) => {
    // Clear the error as the user didn't initiate this run
    status.value['ollama'].error = null
  })
  await check_api_key_providers()
})
</script>
<template>
    <AppPage>
      <div class="w-full">
        <div class="w-full flex flex-col gap-6 max-w-lg mb-6">
          <div class="flex flex-row gap-4 items-center">
            <img
              :src="provider.image"
              :alt="provider.name"
              :class="[provider.featured ? 'size-12' : 'size-10 mx-1', 'flex-none p-1 ']"
            />
            <div class="flex flex-col grow pr-4">
              <h3>
                {{ provider.name }}
                <div class="badge badge-neutral ml-2 text-xs font-medium">推荐</div>
                <div class="badge badge-soft badge-success ml-2 text-xs font-medium">免费</div>
              </h3>
              <p
                v-if="status[provider.id] && status[provider.id].error"
                class="text-sm text-error"
              >
                {{ status[provider.id].error }}
              </p>
              <p v-else class="text-sm text-gray-500 mt-1">
                {{ status[provider.id].custom_description }}
              </p>
              <button
                v-if="status[provider.id] && status[provider.id].error"
                class="link text-left text-sm text-gray-500"
                @click="show_custom_ollama_url_dialog"
              >
                自定义 Ollama URL
              </button>
              <a :href="provider.provider_url" class="link text-sm mt-1" target="_blank">前往下载</a>
            </div>
            <!-- <div v-if="status[provider.id].connecting" class="btn md:min-w-[100px]">
              <div class="loading loading-spinner loading-md"></div>
            </div> -->
            <div
              v-if="status[provider.id] && status[provider.id].connected"
              class="btn md:min-w-[100px]"
            >
              <CheckCircleIcon class="size-6" alt="Connected" />
            </div>
            <div v-else-if="initial_load_failure">
              <div class="btn md:min-w-[100px] btn-error text-xs text-white">错误</div>
              <div class="text-xs text-gray-500 text-center pt-1">请刷新页面</div>
            </div>
            <button v-else class="btn btn-soft md:min-w-[100px]" @click="connect_ollama()">
              连接
            </button>
          </div>
        </div>
        <div
          v-for="provider in api_key_providers"
          :key="provider.id"
          class="w-full flex flex-col gap-6 max-w-lg mb-6"
        >
          <div class="flex flex-row gap-4 items-center">
            <img
              :src="provider.image"
              :alt="provider.name"
              :class="['size-10 mx-1', 'flex-none p-1 ']"
            />
            <div class="flex flex-col grow pr-4">
              <h3>
                {{ provider.name }}
                <div v-if="provider.featured" class="badge badge-neutral ml-2 text-xs font-medium">
                  推荐
                </div>
                <div v-if="provider.free" class="badge badge-soft badge-success ml-2 text-xs font-medium">限量免费</div>
              </h3>
              <p v-if="status[provider.id] && status[provider.id].error" class="text-sm text-error">
                {{ status[provider.id].error }}
              </p>
              <p class="text-sm text-gray-500 mt-1">
                {{ provider.description }} <a :href="provider.provider_url" target="_blank" class="link text-sm">获取</a>
              </p>
            </div>
            <button
              v-if="status[provider.id].connected"
              class="btn md:min-w-[100px] hover:btn-error group"
              @click="disconnect_provider(provider.id)"
            >
              <CheckCircleIcon class="size-6 group-hover:hidden" alt="Connected" />
              <span class="text-xs hidden group-hover:inline text-white">断开连接</span>
            </button>
            <div
              v-else-if="loading_initial_providers"
              class="btn md:min-w-[100px] skeleton bg-base-200"
            ></div>
            <button v-else class="btn btn-soft md:min-w-[100px]" @click="opendialog(provider)">
              连接
            </button>
          </div>
        </div>
      </div>
      <dialog id="ollama_dialog" class="modal">
        <div class="modal-box">
          <form method="dialog">
            <button
              class="btn btn-sm text-xl btn-circle btn-ghost absolute right-2 top-2 focus:outline-none"
            >
              ✕
            </button>
          </form>

          <h3 class="text-lg font-bold">自定义 Ollama URL</h3>
          <p class="text-sm font-light mb-8">
            默认情况下，软件尝试连接到运行在localhost:11434上的 Ollama.
            如果您在自定义URL或端口上运行 Ollama，请在此处输入以进行连接.
          </p>
          <input
            type="text"
            placeholder="http://localhost:11434"
            v-model="custom_ollama_url"
            class="input input-bordered w-full max-w-[300px]"
          />
          <div class="flex flex-row gap-4 items-center mt-4 justify-end">
            <form method="dialog">
              <button class="btn">取消</button>
            </form>
          </div>
        </div>
        <form method="dialog" class="modal-backdrop">
          <button>关闭</button>
        </form>
      </dialog>
      <dialog id="api_modal" class="modal">
        <div class="modal-box">
          <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
          <h3 class="text-lg font-bold mb-4">{{ current_provider.name }} API Key</h3>
          <p class="text-sm font-light mb-8">您需要 API Key 才能使用此模型.</p>
          <input
            type="text"
            placeholder="请输入 API Key"
            v-model="input_api_key"
            class="input input-bordered w-full max-w-[300px]"
          />
          <div class="modal-action">
            <button class="btn" @click="connect_api_key_providers">连接</button>
          </div>
        </div>
      </dialog>
    </AppPage>
</template>
