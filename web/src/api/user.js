import request from '@/utils/request'

export function login(data) {
  console.log({
    url: '/user/login',
    method: 'post',
    data:{
      data
    }
  })
  return request({
    url: '/user/login',
    method: 'post',
    data:{
      data
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

// export function logout() {
//   return request({
//     url: '/api/auth/logout',
//     method: 'post'
//   })
// }
