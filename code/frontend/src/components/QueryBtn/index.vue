<template>
  <span class="drawerbtn" v-divDrag="dragAlongside">
    <el-button-group>
      <el-button
        circle
        type="primary"
        @click="showDrawer"
        icon="el-icon-thumb"
      ></el-button>
      <transition name="el-zoom-in-center">
        <el-input
          v-show="showInput"
          @mouseleave="showInput = false"
          style="float: left; width: 300px"
          placeholder="          关   键   字   搜   索          "
          v-model="queryKey"
          @keyup.enter="handleQuery"
        ></el-input>
      </transition>
      <el-button
        circle
        @mouseover="showInput = true"
        @click="handleQuery"
        icon="el-icon-search"
      ></el-button>
    </el-button-group>
  </span>
  <query-form ref="queryFormRef"></query-form>
</template>

<script>
import QueryForm from "././QueryForm";
export default {
  name: "QueryBtn",
  components: {
    QueryForm,
  },
  data() {
    return {
      showInput: false,
      queryKey: "",
    };
  },
  computed: {
    dragAlongside() {
      if (!this.showInput){
        return "yl"
      }else {
        return ""
      }
    }
  },
  methods: {
    showDrawer() {
      this.$refs.queryFormRef.drawer = true;
    },
    handleQuery() {
      if (this.showInput){
        this.$store.commit("SET_GLOBALQUERYKEY", this.queryKey.toLowerCase());
        this.$store.commit("SET_COMMITQUERY", true);
      }
    }
  },
};
</script>

<style scoped>
.drawerbtn {
  position: fixed;
  top: 90px;
  left: 5px;
  opacity: 0.8;
  z-index: 90;
  display: inline-block;
  white-space: nowrap; /*强制span不换行*/
}
</style>