import request from '@/utils/request'

function ollamaConnect(data: string | null) {
  return request.client.get('/api/provider/ollama/connect', {
    params: {
      custom_ollama_url: data,
    },
  })
}

function apiKeyProviderStatus() {
  return request.client.get('/api/provider/llm/status')
}

function disconnect(data: string) {
  return request.client.get('/api/provider/llm/disconnect', {
    params: {
      provider_name: data,
    },
  })
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function apiKeyProviderConnect(data: any) {
  return request.client.post('/api/provider/llm/connect', data)
}

function availableModels() {
  return request.client.get('/api/provider/available_models')
}
export default {
  ollamaConnect,
  apiKeyProviderStatus,
  disconnect,
  apiKeyProviderConnect,
  availableModels,
}
