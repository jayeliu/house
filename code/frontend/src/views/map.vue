<template>
  <query-btn></query-btn>
  <div
    v-if="heatmap.visible"
    ref="heatMapCtl"
    class="heatMapCtl horizontal-center"
  >
    <form>
      <label>热点半径：</label>
      <input v-model="heatmap.radius" type="range" min="10" max="80" step="1" />
      <label>模糊尺寸：</label>
      <input v-model="heatmap.blur" type="range" min="10" max="80" step="1" />
    </form>
  </div>
  <map-canvas
    ref="mapCanvasRef"
    @heatMap="handleHeatmap"
    @hoverOn="clickCoord = $event"
  ></map-canvas>
  <map-layer-selection></map-layer-selection>
  <div ref="mapFooterRef" class="footer-left">{{ clickCoord }}</div>
</template>

<script>
import QueryBtn from "@/components/QueryBtn";
import MapCanvas from "@/components/MapCanvas";
import MapLayerSelection from "@/components/MapLayerSelection";

export default {
  name: "Map",
  components: {
    QueryBtn,
    MapCanvas,
    MapLayerSelection,
  },
  data() {
    return {
      heatmap: {
        visible: false,
        radius: 40,
        blur: 40,
      },
      clickCoord: undefined,
    };
  },
  methods: {
    handleHeatmap(heatMapProps) {
      this.heatmap.visible = heatMapProps.visible;
      this.heatmap.radius = heatMapProps.radius;
      this.heatmap.blur = heatMapProps.blur;
    },
  },
  watch: {
    heatmap: {
      handler(val) {
        this.$refs.mapCanvasRef.setHeatMap(val.radius, val.blur);
      },
      deep: true
    },
  },
};
</script>

<style scoped>
.heatMapCtl {
  position: absolute;
  height: 30px;
  background: white;
  opacity: 0.8;
  top: 50px;
  width: 500px;
  z-index: 1000;
}
.footer-left {
  position: absolute;
  height: 30px;
  background: white;
  opacity: 0.8;
  bottom: 0;
  left: 5px;
  z-index: 1000;
}
</style>