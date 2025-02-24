import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import Vue3Lottie from 'vue3-lottie'
const app = createApp(App)
app.use(Vue3Lottie, { name: 'Vue3Lottie' })
app.use(createPinia())
app.use(router)

app.mount('#app')
