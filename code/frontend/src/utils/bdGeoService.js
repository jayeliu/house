// 百度api
import axios from "axios"
// const ak = 'BQl3GjTCdMgaK6pig86Z4aEE5G4EUYHv'  //my
const ak = 'OsxPdYYCZlnhoar9L42cbLvzXxHYi6aR'

export function getLocation(callback) {
  var script = document.createElement('script')
  script.src = `http://api.map.baidu.com/api?v=2.0&ak=${ak}&callback=${callback}`
  document.body.appendChild(script)
}

export function geocoding(address, city, ret_coordtype) {
  return axios({
    url: process.env.VUE_APP_ROOT_API+'geoCoding',
    params: {
      address: address,
      city: city,
      output: 'json',
      ret_coordtype: ret_coordtype,  //国测局经纬度坐标或百度米制坐标----gcj02ll（国测局坐标）、bd09mc（百度墨卡托坐标）、bd09ll（百度经纬度坐标）【默认】
      ak: ak,
    }
  })
}