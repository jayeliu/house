<template>
  <el-menu
    :default-active="activeIndex"
    mode="horizontal"
    text-color="rgb(158, 194, 216)"
    active-text-color="rgb(74, 129, 163)"
    @select="handleSelect"
  >
    <el-menu-item index="1">房源列表</el-menu-item>
    <el-submenu index="2">
      <template #title>个人空间</template>
      <el-menu-item index="2-1">资料卡</el-menu-item>
      <el-menu-item index="2-2">收藏列表</el-menu-item>
    </el-submenu>
    <el-menu-item index="3" disabled>消息中心</el-menu-item>
    <el-menu-item index="4">房源地图</el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: "NavManuHeader",
  data() {
    return {
      activeIndex: "1",
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      switch (key) {
        case "4":
          this.$router.push({
            path: "/map",
          });
          break;
        default:
          console.log(key, keyPath);
      }
    },
  },
};
</script>
