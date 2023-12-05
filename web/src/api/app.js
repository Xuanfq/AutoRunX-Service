import request from '@/utils/request'

export function getApp(query) {
  return request({
    url: '/app/get',
    method: 'get',
    params: query
  })
}

export function addApp(data) {
  return request({
    url: '/app/add',
    method: 'post',
    data
  })
}

export function deleteApp(data) {
  return request({
    url: '/app/delete',
    method: 'post',
    data
  })
}

export function updateAppName(data) {
  return request({
    url: '/app/update/name',
    method: 'post',
    data
  })
}

export function updateAppMark(data) {
  return request({
    url: '/app/update/mark',
    method: 'post',
    data
  })
}

export function updateAppRunconfigUpload(id, data) {
  return request({
    url: '/app/update/runconfig/upload?id=' + id,
    method: 'post',
    data
  })
}

export function updateAppRunconfigDelete(data) {
  return request({
    url: '/app/update/runconfig/delete',
    method: 'post',
    data
  })
}

export function updateAppPlanstart(data) {
  return request({
    url: '/app/update/planstart',
    method: 'post',
    data
  })
}

export function updateAppStart(data) {
  return request({
    url: '/app/update/start',
    method: 'post',
    data
  })
}

export function updateAppAbort(data) {
  return request({
    url: '/app/update/abort',
    method: 'post',
    data
  })
}


export function downloadAppRusult(params) {
  return request({
    url: '/app/download/result',
    method: 'get',
    params: params,
    responseType: 'blob'
  })
}

