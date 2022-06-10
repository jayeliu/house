import axios from "axios"

export function getAddress(code) {
  return axios({
    url: process.env.VUE_APP_ROOT_API+'addressSelection',
    method: 'get',
    params: {
      code: code
    }
  })
}