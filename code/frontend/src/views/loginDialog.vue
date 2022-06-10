<template>
  <section v-show="loginDialogVisible">
    <el-row
      type="flex"
      justify="center"
      @keyup.esc="closeLoginDialog"
      v-loading.fullscreen.lock="fullscreenLoading"
    >
      <div style="float: right">
        <el-button-group>
          <el-button
            round
            icon="el-icon-minus"
            @click="loginDialogVisible = false"
          ></el-button>
          <el-button
            round
            icon="el-icon-close"
            @click="closeLoginDialog"
          ></el-button>
        </el-button-group>
      </div>
      <el-col class="loginDialog" :xs="20" :sm="16" :md="14">
        <header>
          <el-avatar
            shape="square"
            :size="50"
            icon="el-icon-user-solid"
          ></el-avatar>
        </header>
        <el-form
          ref="loginFormRef"
          label-position="left"
          label-width="60px"
          :rules="rulesForm"
          :model="loginForm"
        >
          <el-form-item label="账号:" prop="username">
            <el-input
              v-model="loginForm.username"
              prefix-icon="el-icon-user"
              placeholder="请输入账号"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="password">
            <el-input
              v-model="loginForm.password"
              prefix-icon="el-icon-mouse"
              placeholder="请输入密码"
              show-password
              @keyup.enter="handleLogin"
              autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-form>
        <footer>
          <el-button @click="handleRegister">注 册</el-button>
          <el-button type="primary" @click="handleLogin">登 录</el-button>
        </footer>
      </el-col>
    </el-row>
  </section>
</template>

<script>
import { containMultiChar } from "@/utils/utils";
import { getVerificationCodeImg } from "@/api/login";

export default {
  name: "LoginDialog",
  data() {
    return {
      loginDialogVisible: false,
      fullscreenLoading: false,
      loginForm: {
        username: "",
        password: "",
      },
      // 假数据
      passLoginForm:{
        username: "admin",
        password: "admin@123",
      },
      rulesForm: {
        username: [
          {
            validator: (rule, value, callback) => {
              // 用户名校验规则：1.不能为空；2.不能少于5个字符
              if (value === "") {
                callback(new Error("请输入账号"));
              } else if (value.length < 5) {
                callback(new Error("账号长度至少5个字符"));
              } else {
                callback();
              }
            },
            trigger: "blur",
          },
        ],
        password: [
          {
            validator: (rule, value, callback) => {
              // 密码校验规则：1.不能为空；2.不能少于6个字符；3.至少包含三种不同类型的字符（正则校验）
              if (value === "") {
                callback(new Error("请输入密码"));
              } else {
                this.$refs.loginFormRef.validateField("username");
                if (value.length < 6) {
                  callback(new Error("密码长度至少6个字符"));
                } else if (!containMultiChar(value)) {
                  callback(new Error("密码需至少包含三种不同类型的字符"));
                } else {
                  callback();
                }
                callback();
              }
            },
            trigger: "blur",
          },
        ],
      },
    };
  },
  computed: {},
  created() {},
  methods: {
    closeLoginDialog() {
      this.loginDialogVisible = false;
      this.$refs.loginFormRef.resetFields();
    },
    handleRegister() {
      console.log("register");
      this.loginDialogVisible = false;
    },
    handleLogin() {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          this.fullscreenLoading = true;
          // 假验证
          if (this.loginForm.username == this.passLoginForm.username && this.loginForm.password == this.passLoginForm.password){
            this.$emit('loadUserData', {
              userUnId: 'admin',
              userPhotoUrl: "https://pic.qqtn.com/up/2019-1/2019010208201525732.jpg",
              userCity: '北京市',
              userAddr: '中国科学院大学',
            })
            this.fullscreenLoading = false;
            this.$message({
              type: "success",
              duration: 800,
              message: "登录成功",
            });
            this.loginDialogVisible = false
          }else {
            this.fullscreenLoading = false;
            this.$message({
              type: "error",
              duration: 800,
              message: "账号或密码错误！",
            });
          }
        }
      });
    },
  },
  watch: {
    loginDialogVisible() {},
  },
};
</script>

<style scoped>
section {
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: 1000;
  top: 0;
  background: rgba(176, 197, 243, 0.4);
}
.loginDialog {
  position: fixed;
  z-index: 1001;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.12);
  margin-top: 180px;
  border-radius: 8px;
  background: white;
  padding-right: 3%;
  padding-left: 3%;
  text-align: center;
}
header {
  margin-top: 8%;
  margin-bottom: 20px;
}
footer {
  margin-top: 15%;
  margin-bottom: 20px;
}
</style>