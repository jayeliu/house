<template>
  <el-pagination
    :currentPage="currentPage"
    :page-sizes="[15, 20, 30, 40]"
    :page-size="pageSize"
    :page-count="pageCount"
    layout="sizes, prev, pager, next, jumper"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
  >
  </el-pagination>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Pagination",
  computed: {
    ...mapGetters(["pageCount"]),
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 20,
    };
  },
  methods: {
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
  },
  watch: {
    currentPage(val) {
      this.$store.commit("SET_CURRENTPAGE", val);
    },
    pageSize(val) {
      this.$store.commit("SET_PAGESIZE", val);
    },
  },
};
</script>
