import axios from "axios"

export function getBublelist(params) {
  return axios({
    url: process.env.VUE_APP_ROOT_API+'bublelist',
    method: 'get',
    params: params
  })
}