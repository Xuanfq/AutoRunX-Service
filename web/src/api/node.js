import request from '@/utils/request'

export function getNodeConfig(query) {
  return request({
    url: '/node/getconfig',
    method: 'get',
    params: query
  })
}

export function getNodeReadme(query) {
  return request({
    url: '/node/getreadme',
    method: 'get',
    params: query
  })
}

export function addNodes(data) {
  return request({
    url: '/node/add',
    method: 'post',
    data
  })
}

export function syncNodes(data) {
  return request({
    url: '/node/sync',
    method: 'post',
    data
  })
}

export function deleteNodes(data) {
  return request({
    url: '/node/delete',
    method: 'post',
    data
  })
}
