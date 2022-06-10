<template>
  <span>
    <el-select
      style="width: 150px"
      v-model="globalCityCode"
      clearable
      placeholder="请选择城市"
      size="small"
    >
      <el-option
        v-for="item in globalCityOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      >
      </el-option>
    </el-select>
    <el-button
      size="mini"
      @click="handleGetLocation"
      icon="el-icon-location-information"
      v-loading.fullscreen.lock="positioning"
      element-loading-text="定位中..."
      circle
    ></el-button>
  </span>
</template>

<script>
import { mapGetters } from "vuex";
import { getLocation, geocoding } from "@/utils/bdGeoService";

export default {
  name: "GetLocation",
  computed:{
    ...mapGetters(["locationCityCode"]),
  },
  data() {
    return {
      globalCityOptions: [
        //{ value: "A420100000", label: "武汉市" },
        { value: "A311000000", label: "上海市" },
        { value: "A111000000", label: "北京市" },
      ],
      globalCityCode: "",

      BMap: null,
      geolocation: null, // Geolocation对象实例
      positioning: false, // 定位中
      positioningInterval: null, // 定位倒计时计时器
      countDown: 30, // 倒计时，单位秒
      location: {}, // 定位信息
      getLocationCity: "", // 定位城市
    };
  },
  created() {
    this.globalCityCode = this.locationCityCode;
  },
  mounted() {
    const _this = this;
    window.initBaiduMapScript = () => {
      _this.BMap = window.BMap;
    };
    getLocation("initBaiduMapScript");
  },
  methods: {
    handleGetLocation() {
      const _this = this;
      this.$confirm("需要获取您的位置信息", "位置授权", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          _this.getLocation();
        })
        .catch(() => {
          this.$message({
            type: "error",
            duration: 800,
            message: "位置授权失败",
          });
        });
    },
    // 获取地理定位
    getLocation() {
      const _this = this;
      _this.geolocation = new _this.BMap.Geolocation();
      if (_this.geolocation) {
        // 开启SDK辅助定位，仅当使用环境为移动web混合开发，且开启了定位sdk辅助定位功能后生效
        _this.geolocation.enableSDKLocation();
        // 开始定位
        this.positioning = true;
        // 倒计时
        this.positioningInterval = setInterval(() => {
          if (this.countDown === 0) {
            this.countDown = 30;
            clearInterval(this.positioningInterval);
          } else {
            this.countDown--;
          }
        }, 1000);
        // 位置选项
        const positionOptions = {
          enableHighAccuracy: true, // 要求浏览器获取最佳结果
          timeout: 3, //    超时时间
          maximumAge: 0, // 允许返回指定时间内的缓存结果。如果此值为0，则浏览器将立即获取新定位结果
        };
        // 获取用户位置信息
        _this.geolocation.getCurrentPosition((position) => {
          _this.resetPositioning();
          // 获取定位结果状态码
          const statusCode = _this.geolocation.getStatus();
          let msg = "由于未知错误而无法检索设备的位置"; // 提示消息
          let msgType = "error"; // 消息类型
          // 判断结果状态码，为0代表获取成功，读取省市、经纬度
          switch (statusCode) {
            case 0:
              msgType = "success";
              msg = "获取地理位置定位请求成功";
              if (position) {
                // 数据变量定义
                let lat = 0.0; // 经度
                let lng = 0.0; // 纬度
                let province = "未知"; // 经度
                let city = "未知"; // 纬度

                // 坐标
                if (position.point) {
                  lat = position.point.lat;
                  lng = position.point.lng;
                }
                // 位置
                if (position.address) {
                  province = position.address.province;
                  city = position.address.city;
                }
                _this.location = {
                  province: province,
                  city: city,
                  lat: lat,
                  lng: lng,
                };
                _this.getLocationCity = city;
              } else {
                msg = "由于未知错误而无法检索设备的位置";
              }
              break;
            case 2:
              msg = "由于未知错误而无法检索设备的位置";
              break;
            case 4:
            case 5:
              msg = "位置服务请求非法";
              break;
            case 6:
              msg = "应用程序没有使用位置服务的权限";
              break;
            case 7:
              msg = "网络不可用或者无法连接到获取位置信息的卫星";
              break;
            case 8:
              msg = "无法在指定的最大超时间隔内检索位置信息";
              break;
            default:
              msg = "由于未知错误而无法检索设备的位置";
              break;
          }
          _this.$message({
            type: msgType,
            message: msg,
          });
        }, positionOptions);
      } else {
        _this.$message({
          type: msgType,
          message: "您的浏览器不支持地理位置服务",
        });
      }
    },
    // 重置定位相关数据
    resetPositioning() {
      this.positioning = false;
      this.location = null;
      this.countDown = 30;
      clearInterval(this.positioningInterval);
    },
  },
  watch: {
    getLocationCity(newVal, oldVal) {
      let globalCityLabels = this.globalCityOptions.map((e) => e.label);
      if (globalCityLabels.includes(newVal)) {
        this.globalCityCode = this.globalCityOptions.filter(
          (e) => e.label == newVal
        )[0].value;
      } else {
        this.$message({
          type: "info",
          dangerouslyUseHTMLString: true,
          message: `暂不支持 <strong style='color: rgb(74, 129, 163)'>${this.getLocationCity}</strong> 地区的房源信息查询`,
        });
        this.globalCityCode = "";
      }
    },
    globalCityCode(val) {
      const _this = this
      if (
        !(
          this.location.hasOwnProperty("lat") &&
          this.location.hasOwnProperty("lng")
        ) &&
        val.length != 0
      ) {
        let address = this.globalCityOptions.filter((e) => e.value == val)[0]
          .label;
        geocoding(address).then((res) => {
          _this.location.lat = res.data.result.location.lat;
          _this.location.lng = res.data.result.location.lng;
        });
        _this.location.city = address;
      }
      this.location.code = val;
      this.$store.commit("SET_CLIENTLOCATION", this.location);
    },
  },
};
</script>
