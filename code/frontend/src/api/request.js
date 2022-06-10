import axios from "axios"
import { Notification, MessageBox, Message } from "element-ui";
import store from "@/store";
import { getToken } from "@/utils/auth";
// import { decryptObjStr } from "@/utils/aesUtil";
import { heat } from "@/api/login";

axios.defaults.headers["Content-Type"] = "application/json;charset=utf-8";
// 创建axios实例
const service = axios.create({
  // axios中请求配置有baseURL选项，表示请求URL公共部分
  baseURL: process.env.VUE_APP_BASE_API,
  // 请求凭证
  withCredentials: true,
  // 超时
  timeout: 60000
});

// request拦截器
service.interceptors.request.use(
  config => {
    if (getToken()) {
      config.headers["Authorization"] = "Bearer " + getToken(); // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    config.headers["X-Requested-With"] = "XMLHttpRequest";
    return config;
  },
  error => {
    console.log(error);
    Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  res => {
    const code = res.data.code;
    const headers = res.headers;
    if (
      headers["content-type"] &&
      headers["content-type"].indexOf("application/octet-stream") != -1
    ) {
      return res;
    }
    if (code === 401) {
      store.dispatch("CleanLoginInfo");
      if (res.data.redirect) {
        location.href = res.data.redirect;
      } else {
        MessageBox.confirm(
          res.data.message ||
            "登录状态已过期，您可以继续留在该页面，或者重新登录",
          "系统提示",
          {
            confirmButtonText: "重新登录",
            type: "warning"
          }
        )
          .then(() => {
            // store.dispatch('LogOut').then(() => {
            //   location.reload() // 为了重新实例化vue-router对象 避免bug
            // })
            heat({ loginType: 2 }).then(() => location.reload());
          })
          .catch(() => {
            heat({ loginType: 1 }).then(() => {
              location.reload();
            });
          });
      }
      return Promise.reject("error");
    } else if (code !== 200) {
      Notification.error({
        title: res.data.message
      });
      return Promise.reject("error");
    } else {
      if (res.data.data) {
        res.data.data = decryptObjStr(res.data.data);
      }
      return res.data;
    }
  },
  error => {
    console.log("err" + error);
    Message({
      message: error.message,
      type: "error",
      duration: 5 * 1000
    });
    return Promise.reject(error);
  }
);

export default service;
