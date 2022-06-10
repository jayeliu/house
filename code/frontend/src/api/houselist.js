import axios from "axios"

export function getHouselist(params) {
  return axios({
    url: process.env.VUE_APP_ROOT_API+'houselist',
    method: 'get',
    params: params
  })
}