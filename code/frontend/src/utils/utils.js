// 是数字的字符串（正则校验）
export function isNumber(val) {
  let regex = /^[0-9]*$/
  return regex.test(val)
}

// 至少包含三种不同类型的字符（正则校验）（0-30位字符）
export function containMultiChar(val) {
  let regex = /^((?=.*[A-Z])(?=.*[a-z])(?=.*\d)|(?=.*[a-z])(?=.*\d)(?=.*[\W])|(?=.*[A-Z])(?=.*\d)(?=.*[\W])|(?=.*[A-Z])(?=.*[a-z])(?=.*[\W])).{0,30}$/;
  return regex.test(val)
}