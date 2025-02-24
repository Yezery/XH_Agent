import { createApp } from 'vue'
import Message from '@/components/common/Message.vue'

export interface MessageInstance {
  info: (title: string, content: string) => void
  success: (title: string, content: string) => void
  warning: (title: string, content: string) => void
  error: (title: string, content: string) => void
}

let instance: any = null

export const useMessage = (): MessageInstance => {
  if (!instance) {
    const div = document.createElement('div')
    document.body.appendChild(div)
    const app = createApp(Message)
    instance = app.mount(div)
  }

  return {
    info: (title: string, content: string) => instance.addMessage(title, content, 'info'),
    success: (title: string, content: string) => instance.addMessage(title, content, 'success'),
    warning: (title: string, content: string) => instance.addMessage(title, content, 'warning'),
    error: (title: string, content: string) => instance.addMessage(title, content, 'error'),
  }
}
