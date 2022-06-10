<template>
  <section>
    <header>
      <el-row
        type="flex"
        align="middle"
        justify="space-between"
        class="vetical-center"
      >
        <!-- logo -->
        <el-col :sm="2" :xs="6" class="text-center">
          <img src="@/assets/logo/icons8-house-80.png" alt="logo" />
        </el-col>
        <!-- 城市获取 -->
        <el-col :sm="4" :xs="12" class="text-center">
          <get-location></get-location>
        </el-col>
        <!-- 头部导航菜单 -->
        <el-col :sm="12" class="hidden-xs-only">
          <nav-manu-header class="menu-header"></nav-manu-header>
        </el-col>
        <!-- 用户 -->
        <el-col v-if="!userData.userUnId" :sm="2" :xs="4" class="text-center">
          <el-button type="text" @click="handleLoginDialog">
            <el-avatar
              shape="square"
              :size="50"
              icon="el-icon-user-solid"
            ></el-avatar>
          </el-button>
        </el-col>
        <el-col v-else :sm="2" :xs="4" class="text-center">
          <el-popover placement="top-start" :width="200" trigger="hover">
            <template #reference>
              <el-button type="text" @click="handleUserInfoPopover">
                <el-avatar
                  shape="square"
                  :size="50"
                  fit="fill"
                  :src="userData.userPhotoUrl"
                ></el-avatar>
              </el-button>
            </template>
            <div style="margin-bottom: 20px">
              <strong style="color: red">个人卡片</strong
              ><span style="float: right">
                <el-button type="primary" size="mini" @click="handleLogout"
                  >登出</el-button
                >
              </span>
            </div>
            <li>用户名：{{ userData.userUnId }}</li>
            <li>所在城市：{{ userData.userCity }}</li>
            <li>地址：{{ userData.userAddr }}</li>
          </el-popover>
        </el-col>
      </el-row>
    </header>

    <main>
      <query-btn></query-btn>
      <el-col :span="24" class="text-center table-btn">
        <el-button-group>
          <el-button
            :disabled="tableBtnDisabled"
            @click="
              dialogVisible = true;
              tableBtn = '导出';
            "
            type="primary"
            icon="el-icon-download"
            >导出</el-button
          >
          <el-button
            :disabled="tableBtnDisabled||!(userData.userUnId)"
            @click="
              dialogVisible = true;
              tableBtn = '收藏';
            "
            icon="el-icon-star-off"
            >收藏</el-button
          >
        </el-button-group>
      </el-col>
      <table-list @selected="handleSelected"></table-list>
    </main>
    <footer>
      <pagination></pagination>
    </footer>
    <login-dialog
      ref="loginDialogRef"
      @loadUserData="loadUserData"
    ></login-dialog>
    <el-dialog v-model="dialogVisible" :title="tableBtn" width="80%" center>
      <h1>
        <strong style="color: red; margin-bottom: 40px"
          >是否{{ tableBtn }}以下列表:</strong
        >
      </h1>
      <el-table :data="tableSelection" style="width: 100%" height="350" border>
        <el-table-column prop="title" label="标题" align="center">
        </el-table-column>
        <el-table-column prop="desc" label="描述" align="center">
        </el-table-column>
        <el-table-column prop="priceStr" label="总价" align="center">
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button
          v-if="tableBtn == '导出'"
          type="primary"
          @click="handleExport"
          >确 定</el-button
        >
        <el-button
          v-if="tableBtn == '收藏'"
          type="primary"
          @click="handleCollection"
          >确 定</el-button
        >
      </template>
    </el-dialog>
  </section>
</template>

<script>
import { mapGetters } from "vuex";
import NavManuHeader from "@/components/NavManuHeader";
import GetLocation from "@/components/GetLocation";
import QueryBtn from "@/components/QueryBtn";
import TableList from "@/components/TableList";
import Pagination from "@/components/Pagination";
import LoginDialog from "./loginDialog";

export default {
  name: "TableView",
  components: {
    NavManuHeader,
    GetLocation,
    LoginDialog,
    QueryBtn,
    TableList,
    Pagination,
  },
  computed: {
    ...mapGetters(["clientLocationCoords"]),
  },
  data() {
    return {
      loginDialogVisible: false,
      userData: {
        userUnId: undefined,
      },
      tableBtnDisabled: true,
      tableBtn: undefined,
      tableSelection: [],
      dialogVisible: false,
    };
  },
  created() {},
  computed: {},
  methods: {
    handleLoginDialog() {
      this.$refs.loginDialogRef.loginDialogVisible = true;
    },
    handleLogout() {
      this.userData = {
        userUnId: undefined,
      };
    },
    handleUserInfoPopover() {
      console.log("userifo");
    },
    loadUserData(userData) {
      this.userData = userData;
    },
    handleSelected(selection) {
      if (selection.length) {
        this.tableBtnDisabled = false;
        this.tableSelection = selection;
      } else {
        this.tableBtnDisabled = true;
      }
    },
    handleExport() {
      this.dialogVisible = false
    },
    handleCollection() {
      this.dialogVisible = false
    },
  },
  watch: {},
};
</script>

<style scoped>
section {
  width: 100%;
  height: 100%;
}
header {
  width: 100%;
  padding-top: 2px;
  height: 65px;
  margin: 0;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.12);
}
main {
  width: 100%;
}
footer {
  height: 40px;
  opacity: 0.9;
  bottom: 0;
  position: fixed;
  z-index: 999;
}
.menu-header {
  bottom: 0;
}
.table-btn {
  margin-top: 30px;
  margin-bottom: 10px;
  margin-right: 30px;
  float: right;
}
</style>