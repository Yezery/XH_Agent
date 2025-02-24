import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/worker',
    },
    {
      path: '/worker',
      name: '工作区',
      component: () => import('../views/WorkerView.vue'),
    },
    {
      path: '/settings',
      name: '设置',
      component: () => import('../views/Setting/SettingMainView.vue'),
    },
    {
      path: '/settings/providers',
      name: 'AI 模型',
      component: () => import('../views/Setting/ProvidersView.vue'),
    },
    {
      path: '/settings/check_for_update',
      name: '检查更新',
      component: () => import('../views/Setting/CheckForUpdateView.vue'),
    },
    {
      path: '/settings/system_cache',
      name: '系统缓存',
      component: () => import('../views/Setting/SystemCache.vue'),
    },
  ],
})

export default router
