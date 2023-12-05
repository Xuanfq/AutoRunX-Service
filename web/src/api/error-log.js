import request from '@/utils/request'

export function getErrorLog(query) {
  return request({
    url: '/errorlog/get',
    method: 'get',
    params: query
  })
}