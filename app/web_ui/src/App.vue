<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, watchEffect } from 'vue'
import router from './router'
import { Section, type NavigatorType } from './types/app'
import { PencilSquareIcon, Cog6ToothIcon, Bars3Icon } from '@heroicons/vue/20/solid'
const settingsSections = [
  Section.SettingsMain,
  Section.SettingsProviders,
  Section.SettingsAppUpdate,
  Section.SettingSystemCache,
]
function path_start(root: string, pathname: string): boolean {
  if (pathname == root) {
    return true
  } else if (pathname.startsWith(root + '/')) {
    return true
  }
  return false
}
const section = ref(Section.None)
watchEffect(() => {
  const url = router.currentRoute.value.fullPath
  if (path_start('/worker', url)) {
    section.value = Section.WORKER
  } else if (path_start('/settings/providers', url)) {
    section.value = Section.SettingsProviders
  } else if (path_start('/settings/check_for_update', url)) {
    section.value = Section.SettingsAppUpdate
  } else if (path_start('/settings/system_cache', url)) {
    section.value = Section.SettingSystemCache
  } else if (path_start('/settings', url)) {
    section.value = Section.SettingsMain
  } else {
    section.value = Section.None
  }
})

const navigator: NavigatorType[] = [
  {
    to: '/worker',
    title: '工作区',
    icon: PencilSquareIcon,
    section: Section.WORKER,
  },
  {
    to: '/settings',
    title: '设置',
    icon: Cog6ToothIcon,
    section: Section.SettingsMain,
    subsections: [
      {
        to: '/settings/providers',
        title: 'AI 模型',
        section: Section.SettingsProviders,
      },
      {
        to: '/settings/check_for_update',
        title: '检查更新',
        section: Section.SettingsAppUpdate,
      },
      {
        to: '/settings/system_cache',
        title: '系统缓存',
        section: Section.SettingSystemCache,
      },
    ],
  },
]
</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="main-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col lg:mr-4 min-h-screen">
      <div class="flex-none h-12 lg:h-6">
        <div class="flex flex-row h-full items-center">
          <label for="main-drawer" class="drawer-button lg:hidden">
            <Bars3Icon class="size-6 mx-3"></Bars3Icon>
          </label>
          <div class="flex-grow lg:hidden">
            {{ router.currentRoute.value.name }}
          </div>
        </div>
      </div>

      <div
        class="flex-grow rounded-3xl bg-base-100 shadow-md px-4 md:px-12 py-8 mb-4 outline-1 -outline-offset-1 outline-gray-100"
      >
       <RouterView />
      </div>
    </div>
    <div class="drawer-side" role="navigation">
      <label for="main-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu bg-base-200 text-base-content min-h-full w-72 lg:w-72 p-4 pt-1 lg:pt-4">
        <div class="mb-4 ml-4 mt-2">
          <div class="flex flex-row items-center mx-[-5px] p-0">
            <img src="/images/logo.png" alt="logo" class="w-8 h-8" />
            <div class="text-lg font-bold ml-1">XH Agent</div>
          </div>
        </div>

        <li class="menu-lg" v-for="nav in navigator" :key="nav.to">
          <RouterLink
            :to="nav.to"
            :class="[section == nav.section ? 'menu-active' : '', 'pt-3 pb-3 mb-1 rounded-xl']"
          >
            <component :is="nav.icon" class="w-6 h-6 mr-2" />
            {{ nav.title }}</RouterLink
          >
          <ul v-if="settingsSections.includes(section) && nav.subsections" class="py-2 ml-6">
            <li class="menu-nested-md" v-for="sub in nav.subsections" :key="sub.to">
              <RouterLink
                :to="sub.to"
                :class="[
                  section == sub.section ? 'menu-active' : '',
                  'pt-2 pb-2 mb-1 rounded-lg text-sm',
                ]"
              >
                {{ sub.title }}
              </RouterLink>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
:global(ul > li.menu-nested-sm) {
  padding: 0.1rem 0.25rem;
}
:global(ul > li.menu-nested-sm > a) {
  padding: 0.2rem 1rem;
  font-size: 0.875rem;
}
</style>
