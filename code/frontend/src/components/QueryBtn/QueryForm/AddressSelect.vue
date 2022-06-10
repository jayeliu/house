<template>
  <span>
    <el-form-item label="行政区划" prop="district">
      <el-select v-model="queryParams.district" clearable filterable>
        <el-option
          v-for="item in districtOptions"
          :label="item.dictLabel"
          :value="item.dictValue"
          :key="item.dictLabel"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="街道" prop="street">
      <el-select v-model="queryParams.street" multiple clearable filterable>
        <el-option
          v-for="item in streetOptions"
          :label="item.dictLabel"
          :value="item.dictValue"
          :key="item.dictLabel"
        ></el-option>
      </el-select>
    </el-form-item>
    <!-- <el-form-item label="小区" prop="neighbourhood">
      <el-select v-model="queryParams.neighbourhood" multiple clearable filterable>
        <el-option
          v-for="item in neighbourhoodOptions"
          :label="item.dictLabel"
          :value="item.dictValue"
          :key="item.dictLabel"
        ></el-option>
      </el-select>
    </el-form-item> -->
  </span>
</template>
<script>
import {getAddress} from "@/api/addressSelect";
export default {
  name: "AddressSelect",
  props: { queryParams: Object },
  computed: {
    city() {
      return this.queryParams.city;
    },
    district() {
      if (this.queryParams.district) {
        return this.queryParams.district;
      }
    },
    street() {
      if (this.queryParams.street) {
        return this.queryParams.street.join(",");
      }
    },
  },
  data() {
    return {
      districtOptions: [],
      streetOptions: [],
      neighbourhoodOptions: [],
    };
  },
  created() {
    if (this.queryParams.city) {
      this.loadDistrictOptions();
    }
  },
  methods: {
    loadDistrictOptions() {
      if (!this.queryParams.city  || this.queryParams.city.length == 0){
        this.districtOptions = [];
        return
      }
      getAddress(this.queryParams.city).then((res) => {
        res.data.forEach(i => {
          let item = {dictLabel: i.name, dictValue: i.code}
          this.districtOptions.push(item)
        });
      });
    },
    loadStreetOptions() {
      if (!this.queryParams.district || this.queryParams.district.length == 0) {
        this.streetOptions = [];
        return;
      }
      getAddress(this.queryParams.district).then((res) => {
        res.data.forEach(i => {
          let item = {dictLabel: i.name, dictValue: i.code}
          this.streetOptions.push(item)
        })
      });
    },
    loadNeighbourhoodOptions() {
      if (!this.queryParams.street || this.queryParams.street.length == 0) {
        this.neighbourhoodOptions = [];
        return;
      }
      getAddress(this.queryParams.street.join(",")).then((res) => {
        res.data.forEach(i => {
          let item = {dictLabel: i.name, dictValue: i.code}
          this.neighbourhoodOptions.push(item)
        })
      });
    },
  },
  watch: {
    city() {
      this.queryParams.district = undefined;
      this.queryParams.street = undefined;
      this.queryParams.neighbourhood = undefined;
      this.districtOptions = [];
      this.streetOptions = [];
      this.neighbourhoodOptions = [];
      this.loadDistrictOptions();
    },
    district() {
      this.queryParams.street = undefined;
      this.queryParams.neighbourhood = undefined;
      this.streetOptions = [];
      this.neighbourhoodOptions = [];
      this.loadStreetOptions();
    },
    street() {
      this.queryParams.neighbourhood = undefined;
      this.neighbourhoodOptions = [];
      this.loadNeighbourhoodOptions();
    },
  },
};
</script>
