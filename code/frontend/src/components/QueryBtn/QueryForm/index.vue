<template>
  <el-drawer v-model="drawer" direction="ltr" size="400px">
    <el-form
      class="queryform"
      :model="queryParams"
      status-icon
      :rules="rules"
      ref="queryFormRef"
    >
      <address-select :queryParams="queryParams"></address-select>
      <el-form-item label="总价(万元)" prop="priceRange">
        <el-slider
          class="slider"
          :min="10"
          :max="1000"
          range
          v-model="queryParams.priceRange"
          :marks="priceRangeMarks"
        ></el-slider>
      </el-form-item>
      <el-form-item label="单价(元/m²)" prop="unitPriceRange">
        <el-slider
          class="slider"
          :min="5000"
          :max="100000"
          range
          v-model="queryParams.unitPriceRange"
          :marks="unitPriceRangeMarks"
        ></el-slider>
      </el-form-item>
      <el-form-item label="面积(m²)" prop="areaRange">
        <el-slider
          class="slider"
          :min="10"
          :max="300"
          range
          v-model="queryParams.areaRange"
          :marks="areaRangeMarks"
        ></el-slider>
      </el-form-item>
      <el-form-item label="户型" prop="layout">
        <el-select v-model="queryParams.layout" multiple :clearable="true">
          <el-option
            v-for="item in layoutOptions"
            :label="item.dictLabel"
            :value="item.dictValue"
            :key="item.dictLabel"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="类型" prop="cardType">
        <el-select v-model="queryParams.cardType" multiple :clearable="true">
          <el-option
            v-for="item in cardTypeOptions"
            :label="item.dictLabel"
            :value="item.dictValue"
            :key="item.dictLabel"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script>
import { mapGetters } from "vuex";
import AddressSelect from "./AddressSelect";

export default {
  name: "QueryForm",
  components: {
    AddressSelect,
  },
  computed: {
    ...mapGetters(["locationCityCode", "globalQueryParams"]),
  },
  data() {
    return {
      drawer: false,
      rules: [],
      queryParams: {},
      priceRangeMarks: {
        10: "10",
        1000: "1k",
      },
      unitPriceRangeMarks: {
        5000: "5k",
        100000: "10w",
      },
      areaRangeMarks: {
        10: "10",
        300: "300",
      },
      layoutOptions: [
        { dictValue: "5室2厅", dictLabel: "5室2厅" },
        { dictValue: "4室3厅", dictLabel: "4室3厅" },
        { dictValue: "4室2厅", dictLabel: "4室2厅" },
        { dictValue: "3室2厅", dictLabel: "3室2厅" },
        { dictValue: "3室1厅", dictLabel: "3室1厅" },
        { dictValue: "2室2厅", dictLabel: "2室2厅" },
        { dictValue: "2室1厅", dictLabel: "2室1厅" },
        { dictValue: "1室2厅", dictLabel: "1室2厅" },
        { dictValue: "1室1厅", dictLabel: "1室1厅" },
      ],
      cardTypeOptions: [
        { dictValue: "二手房", dictLabel: "二手房" },
      ],
    };
  },
  created() {
    this.queryParams.city = this.locationCityCode;
  },
  methods: {
    submitForm() {
      this.$refs.queryFormRef.validate((valid) => {
        if (valid) {
          this.$store.commit("SET_GLOBALQUERYPARAMS", this.queryParams);
          this.$store.commit("SET_COMMITQUERY", true);
        }
      });
    },
    resetForm() {
      this.queryParams = {
        district: undefined,
        street: undefined,
        neighbourhood: undefined,
        priceRange: [10,1000],
        unitPriceRange: [5000,100000],
        areaRange: [10,300],
        layout: undefined,
        cardType: undefined,
      }
    },
  },
  watch: {
    drawer(val) {
      if (val) {
        if (this.globalQueryParams) {
          this.queryParams = this.globalQueryParams
        }
      } else {
        this.$store.commit("SET_GLOBALQUERYPARAMS", this.queryParams);
      }
    },
    locationCityCode(val) {
      this.queryParams.city = val;
    },
  },
};
</script>

<style scoped>
.queryform {
  text-align: center;
  padding-left: 5%;
}
.slider {
  margin-left: 120px;
  margin-right: 10%;
}
</style>
