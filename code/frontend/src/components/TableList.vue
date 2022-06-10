<template>
  <el-table
    ref="multipleTableRef"
    :data="
      tableData.filter(
        (data) =>
          !search || data.title.toLowerCase().includes(search.toLowerCase())
      )
    "
    stripe
    @row-click="handleSelection"
    @selection-change="handleSelectionChange"
    style="width: 100%; margin-top: 30px"
    v-loading="loadingTable"
  >
    <el-table-column type="selection" width="50" align="center">
    </el-table-column>
    <el-table-column type="index"> </el-table-column>
    <!-- <el-table-column label="概略图" align="center">
      <template #default="scope">
        <img :src="scope.row.coverPic" alt="">
      </template>
    </el-table-column> -->
    <el-table-column prop="title" label="标题" align="center">
    </el-table-column>
    <el-table-column prop="desc" label="描述" align="center"> </el-table-column>
    <el-table-column prop="priceStr" label="总价" align="center">
    </el-table-column>
    <el-table-column prop="unitPriceStr" label="单价" align="center">
    </el-table-column>
    <el-table-column prop="cardType" label="类型" align="center">
    </el-table-column>
    <el-table-column width="90" fixed="right">
      <template #header>
        <el-input
          v-model="search"
          size="mini"
          placeholder="搜索"
          style="width: 85px; transform: translateX(-10%)"
        />
      </template>
      <template #default="scope">
        <div style="margin-bottom: 5px">
          <el-button size="mini" @click="handleToMap(scope.$index, scope.row)"
            >地图</el-button
          >
        </div>
        <div>
          <el-button
            type="primary"
            size="mini"
            @click="handleToDetial(scope.$index, scope.row)"
            >详情</el-button
          >
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { mapGetters } from "vuex";
import { getHouselist } from "@/api/houselist";

export default {
  name: "TableList",
  data() {
    return {
      tableData: [],
      loadingTable: false,
      search: undefined,
      selectItems: [],
    };
  },
  computed: {
    ...mapGetters([
      "globalQueryParams",
      "globalQueryKey",
      "cityId",
      "currentPage",
      "pageSize",
      "commitQueryParamas",
      "globalQueryResblockId",
    ]),
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      if (!this.cityId) {
        return;
      }
      let params = {
        cityId: this.cityId,
        currentPage: this.currentPage,
        pageSize: this.pageSize,
      };
      if (this.globalQueryResblockId){
        params.resblockId = this.globalQueryResblockId
      }
      params.queryParams = this.globalQueryParams;
      params.queryKey = this.globalQueryKey;
      let _this = this;
      this.loadingTable = true;
      getHouselist(params)
        .then((res) => {
          _this.tableData = res.data.data;
          _this.loadingTable = false;
          _this.$store.commit("SET_PAGECOUNT", res.data.pageCount);
          _this.$store.commit("SET_COMMITQUERY", false);
        })
        .catch(() => {
          setTimeout(() => {
            _this.$store.commit("SET_COMMITQUERY", false);
            _this.loadingTable = false;
          }, 3000);
        });
    },
    handleSelection(selection) {
      // this.$refs.multipleTableRef.toggleRowSelection(selection);
    },
    handleSelectionChange(selection) {
      this.$emit("selected", selection);
    },
    handleToMap(index, row) {
      console.log(row.resblockId);
      this.$router.push({
        path: "/map",
      });
    },
    handleToDetial(index, row) {
      window.open(row.actionUrl, "_blank");
    },
  },
  watch: {
    cityId(val) {
      if (val) {
        this.getData();
      }
    },
    currentPage() {
      this.getData();
    },
    pageSize() {
      this.getData();
    },
    commitQueryParamas(val) {
      if (val) {
        this.getData();
      }
    },
  },
};
</script>