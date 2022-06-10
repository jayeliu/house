import { createStore } from 'vuex'

export default createStore({
  state: {
    clientLocation: {"code": 'A111000000'},   // 用户位置信息

    layersInMap: [],    // 地图中所有的图层

    globalQueryParams: undefined,   // 全局查询参数
    globalQueryKey: undefined,     // 全局查询关键字
    globalQueryResblockId: undefined,    // 全局查询resblockId
    commitQueryParamas: false,   // 提交查询参数

    paginationDetial: {
      currentPage: 1,
      pageSize: 20,
      pageCount: 1,
    },   // 分页数据
  },
  mutations: {
    // 用户位置信息
    SET_CLIENTLOCATION: (state, val) => {
      state.clientLocation = val
    },

    // 地图中的图层参数
    SET_LAYERSINMAP: (state, val) => {
      state.layersInMap = val
    },

    // 全局查询参数
    SET_GLOBALQUERYPARAMS: (state, val) => {
      state.globalQueryParams = val
    },
    // 全局查询关键字
    SET_GLOBALQUERYKEY: (state, val) => {
      state.globalQueryKey = val
    },
    // 全局查询resblockId
    SET_GLOBALQUERYRESBLOCKID: (state, val) => {
      state.globalQueryResblockId = val
    },
    // 提交查询参数
    SET_COMMITQUERY: (state, val) => {
      state.commitQueryParamas = val
    },
    
    // 分页
    SET_CURRENTPAGE: (state, val) => {
      state.paginationDetial.currentPage = val
    },
    SET_PAGESIZE: (state, val) => {
      state.paginationDetial.pageSize = val
    },
    SET_PAGECOUNT: (state, val) => {
      state.paginationDetial.pageCount = val
    },
  },
  actions: {
  },
  modules: {
  },
  getters: {
    locationCityCode: state => {      // 城市区位编码（A420100000）
      return state.clientLocation.hasOwnProperty('code') ? state.clientLocation.code : undefined
    },
    cityId: (state, getters) => {        // 城市区位编码（420100）
      switch (getters.locationCityCode) {
        case "A420100000":
          return "420100";
        case "A311000000":
          return "310000";
        case "A111000000":
          return "110000";
        default:
          return
      }
    },
    zoomCenter: state => {           // 地图视窗中心
      return (state.clientLocation.hasOwnProperty('lat') && state.clientLocation.hasOwnProperty('lng')) ? [state.clientLocation.lng, state.clientLocation.lat] : [114.316200103, 30.5810841269]
    },

    layersInMap: state => state.layersInMap,     // 地图中所有初始化加载入的图层

    globalQueryParams: state => state.globalQueryParams,      // 全局查询参数
    globalQueryKey: state => state.globalQueryKey,      // 全局查询关键字
    globalQueryResblockId: state => state.globalQueryResblockId,     // 全局查询resblockId
    commitQueryParamas: state => state.commitQueryParamas,      // 是否提交查询参数

    currentPage: state => state.paginationDetial.currentPage,    // 当前页
    pageSize: state => state.paginationDetial.pageSize,         // 页容量
    pageCount: state => state.paginationDetial.pageCount,        // 页码数
  }
})
