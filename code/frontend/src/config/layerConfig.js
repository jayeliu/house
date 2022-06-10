import TileArcGISRest from 'ol/source/TileArcGISRest'
import OSM from "ol/source/OSM"
import XYZ from 'ol/source/XYZ'

const coverage = [
  {
    title: "baidu_cg",
    label: "百度卫星",
    source: undefined,
  },
  {
    title: "gaode_cg",
    label: "高德卫星",
    source: undefined,
  },
].map(e => {
  e.disabled = e.source ? false : true
  e.checked = e.source ? false : true
  e.opacity = e.checked ? 1 : undefined
})

const basemap = [
  {
    title: "baidu_bm",
    label: "百度地图",
    source: undefined,
  },
  {
    title: "gaode_bm",
    label: "高德地图",
    source: undefined,
  },
  {
    title: "arcgis_bm",
    label: "ArcGIS地图",
    source: new TileArcGISRest({
      url: 'https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer',
      crossOrigin: 'anonymous',
    }),
  },
  {
    title: "osm_bm",
    label: "OSM地图",
    source: new OSM(),
  },
  {
    title: "offline_bm",
    label: "离线地图",
    source: new XYZ({
      url: 'http://127.0.0.1:7080/streetmap/shenzhen/{z}/{x}/{y}.jpg'
    }),
  },
].map(e => {
  e.disabled = e.source ? false : true
  e.checked = e.source ? false : true
  e.opacity = e.checked ? 1 : undefined
})

const outputlayer = [
  {
    title: "house_outl",
    
    label: "房源分布",
    source: undefined,
  },
].map(e => {
  e.disabled = e.source ? false : true
  e.checked = e.source ? false : true
  e.opacity = e.checked ? 1 : undefined
})

// 卫星底图
export function coverage() {
  let coverage = coverage_
  return
}

// 地图底图
export function basemap() {
  return
}

// 输出图层
export function outputlayer() {
  return
}