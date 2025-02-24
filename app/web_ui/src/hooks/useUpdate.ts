import { reactive, ref, onMounted } from 'vue'
import { createAppError, AppError } from '@/utils/AppError'
import { useMessage } from '@/hooks/useMessage'
const message = useMessage()
export const app_version = '0.0.1'

export type UpdateCheckResult = {
  has_update: boolean
  latest_version: string
  link: string
}

export type UpdateState = {
  update_result: UpdateCheckResult | null
  update_loading: boolean
  update_error: AppError | null
}

export const default_update_state: UpdateState = {
  update_result: null,
  update_loading: false,
  update_error: null,
}

export function useUpdate() {
  const updateState = reactive<UpdateState>({ ...default_update_state })

  const update_update_store = async () => {
    let update_result: UpdateCheckResult | null = null
    let update_error: AppError | null = null
    try {
      updateState.update_loading = true
      updateState.update_result = null
      updateState.update_error = null

      const update = await check_for_update()
      if (update instanceof AppError) {
        update_error = update
      } else {
        update_result = update
      }
    } catch (e) {
      update_error = createAppError(e)
    } finally {
      updateState.update_loading = false
      updateState.update_result = update_result
      updateState.update_error = update_error
      if (update_error) {
        message['error'](`检查更新`, `检查失败`)
        return
      }
      if (update_result?.has_update){
        message['success'](`检查更新`, `有新版本更新${update_result.latest_version}`)
      }else{
        message['success'](`检查更新`, `当前已是最新版本`)
      }
    }
  }

  const check_for_update = async (): Promise<UpdateCheckResult | AppError> => {
    try {
      const response = await fetch('https://api.github.com/repos/Yezery/XH_Agent/releases/latest')
      const data = await response.json()
      const html_url = data.html_url
      const full_version = data.tag_name
      if (!html_url || !full_version) {
        return new AppError('更新信息获取失败', [])
      }
      const [version] = full_version.split('-')
      return {
        has_update: semantic_version_compare(version, app_version),
        latest_version: full_version,
        link: html_url,
      }
    } catch (e) {
      return createAppError(e)
    }
  }

  const semantic_version_compare = (a: string, b: string): boolean => {
    // Strip leading 'v' if present
    const clean_a = a.replace(/^v/, '')
    const clean_b = b.replace(/^v/, '')

    const a_parts = clean_a.split('.').map(Number)
    const b_parts = clean_b.split('.').map(Number)

    // Pad shorter array with zeros to match length
    const max_length = Math.max(a_parts.length, b_parts.length)
    while (a_parts.length < max_length) a_parts.push(0)
    while (b_parts.length < max_length) b_parts.push(0)

    // Compare each part from left to right
    for (let i = 0; i < max_length; i++) {
      if (a_parts[i] > b_parts[i]) return true
      if (a_parts[i] < b_parts[i]) return false
    }

    return false // versions are equal
  }


  return {
    updateState,
    update_update_store,
  }
}
