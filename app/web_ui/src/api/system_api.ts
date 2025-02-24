import request from '@/utils/request'

// 获取文件夹下图片的数量与图片文件总大小

function getCacheInfo() {
  return request.client.get('/api/work/cache')
}

function deleteCache(){
  return request.client.get('/api/work/deleteCache')
}


export default {
  getCacheInfo,
  deleteCache
}
