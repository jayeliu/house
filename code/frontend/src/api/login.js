// import "./request"

// 获取验证码
export function getVerificationCodeImg() {
  return request({
    url: '/captchaImage',
    method: 'get'
  })
}