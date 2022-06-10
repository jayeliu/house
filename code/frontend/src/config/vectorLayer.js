import 'ol/ol.css';
import Circle from 'ol/geom/Circle';
import Feature from 'ol/Feature';
import GeoJSON from 'ol/format/GeoJSON';
import { Circle as CircleStyle, Fill, Stroke, Style, Icon, Text } from 'ol/style';
import { Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer, Heatmap as HeatmapLayer } from 'ol/layer';

// GeoJson
export function vectorGeoJson(jsonList, groupType) {
  var geoFeatures = []
  var pointImgStyle = undefined

  jsonList.forEach(json => {
    let geoFeature = {
      'type': 'Feature',
      'properties': json,
      'geometry': {
        'type': 'GeometryCollection',
        'geometries': [
          {
            'type': 'Polygon',
            'coordinates': json.border && json.groupType !== 'community' ? [json.border.split(";").map(i => i.split(","))] : [],
          },
          {
            'type': 'Point',
            'coordinates': [json.lng, json.lat],
          }
        ],
      },
    }
    geoFeatures.push(geoFeature)
  });
  var zindex
  switch (groupType) {
    case 'community':
      zindex = 13
      pointImgStyle = new Icon({
        scale: 0.6,
        offset: [-20, -40],
        offsetOrigin: 'bottom-right',
        size: [100, 100],
        opacity: 1,
        src: require("@/assets/imgs/locate.png")
      })
      break
    default:
      zindex = 11
      pointImgStyle = new CircleStyle({
        radius: 0,
        fill: null,
      })
  }
  // GeoJson地理实体
  var geoObject = {
    'type': 'FeatureCollection',
    'crs': {
      'type': 'name',
      'properties': {
        'name': 'EPSG:4326',
      },
    },
    'features': geoFeatures,
  };
  // GeoJson常规样式（默认）
  var styles = {
    'GeometryCollection': new Style({
      image: pointImgStyle,
      stroke: new Stroke({
        color: 'rgba(143, 38, 17)',
        width: 2,
      }),
      fill: new Fill({
        color: 'rgba(245, 241, 137, 0.1)',
      }),
    }),
  };
  // 矢量源
  var vectorSource = new VectorSource({
    features: new GeoJSON().readFeatures(geoObject),
  });
  // 样式函数
  var styleFunction = function (feature) {
    let style = styles[feature.getGeometry().getType()]
    return style;
  };
  // 矢量图层
  var vectorLayer = new VectorLayer({
    title: groupType,
    zIndex: zindex,
    source: vectorSource,
    style: styleFunction,
  });
  return vectorLayer
}

// 矢量要素高亮
export function vectorHighlight() {
  // 高亮样式
  var highlightStyle = new Style({
    stroke: new Stroke({
      color: '#f00',
      width: 4,
    }),
    fill: new Fill({
      color: 'rgba(255,0,0,0.1)',
    }),
    text: new Text({
      font: '14px 微软雅黑',
      fill: new Fill({
        color: '#000',
      }),
      stroke: new Stroke({
        color: '#f00',
        width: 3,
      }),
    }),
  });
  // 高亮图层
  var highlightOverlay = new VectorLayer({
    zIndex: 100,
    source: new VectorSource(),
    style: function (feature) {
      highlightStyle.getText().setText(feature.get('name') + ' : ' + feature.get('count') + feature.get('countUnit'));
      return highlightStyle;
    },
  });
  return highlightOverlay
}

// 热点图
export function heatMapVector(jsonList, weightField){
  var geoFeatures = []
  jsonList.forEach(json => {
    let geoFeature = {
      'type': 'Feature',
      'properties': json,
      'geometry': {
        'type': 'Point',
        'coordinates': [json.lng, json.lat],
      },
    }
    geoFeatures.push(geoFeature)
  });
  var geoObject = {
    'type': 'FeatureCollection',
    'crs': {
      'type': 'name',
      'properties': {
        'name': 'EPSG:4326',
      },
    },
    'features': geoFeatures,
  };
  var vectorSource = new VectorSource({
    features: new GeoJSON().readFeatures(geoObject),
  });
  var heatMap = new HeatmapLayer({
    title: '热点图',
    zIndex: 12,
    source: vectorSource,
    radius: 30,
    blur: 30,
    weight: function (feature) {
      var weight = parseFloat(feature.get(weightField))
      return weight;
    },
  })
  return heatMap
}