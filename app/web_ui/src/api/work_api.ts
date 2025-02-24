import request from '@/utils/request'

async function docx_upload(data: FormData) {
  return request.client.post('/api/work/upload/docx', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

async function image_upload(data: FormData) {
  return request.client.post('/api/work/upload/image', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
async function delete_image(data: string) {
  return request.client.get('/api/work/delete/image', {
    params: {
      image_name: data,
    },
  })
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function work_run(data: any) {
  return request.client.post('/api/work/run', data, {
    responseType: 'blob',
  })
}

async function loadUserInfo() {
  return request.client.get('/api/work/setting')
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function gen_summary(data: any) {
  return request.stream_client('/api/work/summary', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

async function rewrite(data: any) {
  return request.stream_client('/api/work/rewrite', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export default {
  docx_upload,
  image_upload,
  gen_summary,
  delete_image,
  work_run,
  loadUserInfo,
  rewrite
}
