import type { Component } from 'vue'

export enum Section {
  WORKER = 'Worker',
  SettingsMain = 'SettingsMain',
  SettingsProviders = 'SettingsProviders',
  SettingsAppUpdate = 'SettingsAppUpdate',
  SettingSystemCache = 'SettingSystemCache',
  None = 'None',
}

export type NavigatorType = {
  to: string
  section: Section
  icon?: Component
  title: string
  subsections?: NavigatorType[]
}
