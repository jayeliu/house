<template>
  <div ref="mapCanvasRef" id="mapCanvas" class="mapCanvas"></div>
  <div ref="popupRef" id="popup" class="popup">
    <el-button
      type="text"
      icon="el-icon-close"
      ref="popupCloserRef"
      class="popupCloser"
      @click="closePopup"
    ></el-button>
    <div style="margin-top: 20px" v-if="featureProps" ref="popupContentRef">
      <el-button
        v-if="featureProps.groupType === 'community'"
        size="mini"
        type="primary"
        @click="toTable"
        >查看房源列表</el-button
      >
      <li>
        名 称：
        <el-tag type="success" size="small" style="float: right">{{
          featureProps.name
        }}</el-tag>
      </li>
      <li>
        房源数量：<el-tag type="warning" size="small" style="float: right"
          >{{ featureProps.count }}{{ featureProps.countUnit }}</el-tag
        >
      </li>
      <li>
        房源平均价格：<el-tag type="danger" size="small" style="float: right"
          >{{ featureProps.price }}{{ featureProps.priceUnit }}</el-tag
        >
      </li>
      <li>
        所属城市Id：<el-tag size="small" style="float: right">{{
          featureProps.cityId
        }}</el-tag>
      </li>
      <li>
        中心经纬度：<el-tag type="info" size="small" style="float: right"
          >{{ featureProps.lng }},{{ featureProps.lat }}</el-tag
        >
      </li>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import "ol/ol.css";
import { Map, Overlay } from "ol";
import { toLonLat } from "ol/proj";
import { toStringHDMS } from "ol/coordinate";
import { baseLayers, mapView } from "../config/mapConfig";
import { getBublelist } from "@/api/bublelist";
import {
  vectorGeoJson,
  vectorHighlight,
  heatMapVector,
} from "../config/vectorLayer";

export default {
  name: "MapCanvas",
  emits: ["hoverOn", "heatMap"],
  computed: {
    ...mapGetters(["zoomCenter", "cityId", "layersInMap"]),
    heatMapProps(){
      return this.heatMap?this.heatMap.getProperties():{}
    }
  },
  data() {
    return {
      map: null,
      popup: null, // 弹框气泡
      heatMap: null, // 热力图图层
      pointCoord: undefined, // 鼠标所在经纬度
      popupVisible: true,
      featureProps: undefined, // 所点击要素的属性信息
    };
  },
  created() {
    this.vectorBublelist("district");
    this.vectorBublelist("bizcircle");
    this.vectorBublelist("community");
  },
  mounted() {
    this.map = new Map({
      target: "mapCanvas",
      layers: baseLayers(),
      view: mapView(this.zoomCenter),
    }); // 初始化地图
    this.sentLayersIn(); // 传递当前地图中的图层至图层选择器
    this.initOverlay(); // 初始化弹框气泡
    this.clickFeature(); // 单击要素
    this.highlightFeature(); // 高亮要素
  },
  methods: {
    // 矢量化显示bublelist
    vectorBublelist(groupType) {
      if (!this.cityId) {
        return;
      }
      let params = {
        cityId: this.cityId,
        groupType: groupType,
      };
      let _this = this;
      getBublelist(params).then((res) => {
        if (res.data.length != 0) {
          let vectorLayer = vectorGeoJson(res.data, groupType);
          if (groupType === "community") {
            _this.heatMap = heatMapVector(res.data,'count');
            _this.map.addLayer(_this.heatMap);
          }
          _this.map.addLayer(vectorLayer);
          _this.sentLayersIn();
        }
      });
    },
    // 初始化覆盖层
    initOverlay() {
      let _this = this;
      _this.popup = new Overlay({
        element: _this.$refs.popupRef,
        autoPan: true,
        autoPanAnimation: {
          duration: 250,
        },
      });
      _this.map.addOverlay(_this.popup); // 添加覆盖层popup
    },
    // 单击要素
    clickFeature() {
      let _this = this;
      this.map.on("singleclick", function (evt) {
        var clickCoord = evt.coordinate;
        var pixel = _this.map.getEventPixel(evt.originalEvent);
        var feature = _this.map.forEachFeatureAtPixel(
          pixel,
          function (feature) {
            return feature;
          }
        );
        if (feature) {
          _this.featureProps = feature.getProperties();
          _this.popup.setPosition(clickCoord);
        } else {
          _this.featureProps = undefined;
          _this.closePopup();
        }
      });
    },
    // 高亮要素
    highlightFeature() {
      var _this = this;
      var highlight;
      var highlightOverlay = vectorHighlight();
      this.map.addLayer(highlightOverlay);
      var displayFeatureInfo = function (feature) {
        if (feature !== highlight) {
          if (highlight) {
            highlightOverlay.getSource().removeFeature(highlight);
          }
          if (feature) {
            highlightOverlay.getSource().addFeature(feature);
          }
          highlight = feature;
        }
      };
      this.map.on("pointermove", function (evt) {
        _this.pointCoord = evt.coordinate;
        if (evt.dragging) {
          return;
        }
        var pixel = _this.map.getEventPixel(evt.originalEvent);
        var feature = _this.map.forEachFeatureAtPixel(
          pixel,
          function (feature) {
            return feature;
          }
        );
        displayFeatureInfo(feature);
      });
    },
    // 关闭弹框
    closePopup() {
      this.popup.setPosition(undefined);
    },
    // 设置热点图
    setHeatMap(radius, blur) {
      this.heatMap.setRadius(parseInt(radius))
      this.heatMap.setBlur(parseInt(blur))
    },
    // 传递当前地图中的图层至图层选择器
    sentLayersIn() {
      let layersIn = [];
      this.map.getLayers().forEach((layer) => {
        let layerValues = layer.values_;
        // 有标题的图层（传递至选项节点树中）
        if (layerValues.title) {
          let aLayer_ = {
            // default
            title: layerValues.title, // 图层名
            type: layerValues.type ? layerValues.type : "输出图层", // 图层所属类
            disabled: layerValues.source ? false : true, // 是否可选
            selected: false, // 是否已选
            opacity: layerValues.opacity, // 图层透明度
          };
          if (layerValues.title === "高德地图") {
            // 设置默认高德可见
            aLayer_.selected = true;
          }
          layersIn.push(aLayer_);
        }
      });
      this.$store.commit("SET_LAYERSINMAP", layersIn);
    },
    // 设置图层visible,opacity
    setLayers() {
      let _this = this;
      this.map.getLayers().forEach((layer) => {
        let layerValues = layer.values_;
        // 设置图层可视性和透明度
        let title_ = layerValues.title;
        if (title_) {
          let alayer = _this.layersInMap.filter((i) => i.title === title_);
          if (alayer.length) {
            layer.setVisible(alayer[0].selected);
            layer.setOpacity(parseFloat(alayer[0].opacity));
          } else {
            layer.setVisible(false);
          }
        }
      });
    },
    // 转table
    toTable() {
      this.$store.commit("SET_GLOBALQUERYPARAMS", undefined);
      this.$store.commit("SET_GLOBALQUERYKEY", undefined);
      this.$store.commit("SET_GLOBALQUERYRESBLOCKID", this.featureProps.unId);
      this.$router.push({
        path: "/tableView",
      });
    },
  },
  watch: {
    layersInMap: {
      // 监听图层参数变化
      handler: function (val) {
        this.setLayers();
      },
      deep: true,
    },
    pointCoord(val) {
      // 鼠标悬停位置经纬度
      this.$emit("hoverOn", toStringHDMS(val));
    },
    heatMapProps: {
      // 监听热点图参数变化
      handler: function (val) {
        this.$emit("heatMap", this.heatMapProps);
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.mapCanvas {
  height: 100%;
  width: 100%;
}
.popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 350px;
}
.popup:after,
.popup:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}
.popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}
.popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}
.popupCloser {
  position: absolute;
  top: 0px;
  right: 8px;
}
</style>