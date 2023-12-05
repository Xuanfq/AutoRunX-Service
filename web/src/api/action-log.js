import request from '@/utils/request'

export function getActionLog(query) {
  return request({
    url: '/actionlog/get',
    method: 'get',
    params: query
  })
}