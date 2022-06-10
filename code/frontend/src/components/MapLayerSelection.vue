<template>
  <span class="mapLayerSelection" v-divDrag="dragAlongside">
    <el-popover
      placement="bottom-end"
      title="图层"
      :width="300"
      trigger="click"
      v-model:visible="visible"
    >
      <template #reference>
        <el-button circle icon="el-icon-copy-document"></el-button>
      </template>
      <el-tree
        ref="treeRef"
        :data="treeData"
        node-key="title"
        :default-expanded-keys="['地图底图']"
        :props="defaultProps"
        icon-class="el-icon-folder-opened"
      >
        <template #default="{ data }">
          <span v-if="!data.children">
            <el-checkbox
              v-model="data.selected"
              :disabled="data.disabled"
              @change="updateParentChecked()"
              >{{ data.title }}</el-checkbox
            >
            <span v-if="data.selected">
              <input
                v-model="data.opacity"
                type="range"
                min="0"
                max="1"
                step="0.01"
              />
            </span>
          </span>
          <span v-else>
            <el-checkbox
              :indeterminate="data.indeterminate"
              v-model="data.selected"
              :disabled="data.disabled"
              @change="updateChildrenChecked(data)"
              >{{ data.title }}</el-checkbox
            >
          </span>
        </template>
      </el-tree>
    </el-popover>
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "MapLayerSelection",
  computed: {
    ...mapGetters(["layersInMap"]),
    // 按钮拖拽
    dragAlongside() {
      if (!this.visible) {
        return "";
      } else {
        return "disabled";
      }
    },
  },
  data() {
    return {
      visible: false,
      layersIn: undefined,
      treeData: undefined,
      defaultProps: {
        children: "children",
      }, // 树节点默认属性
    };
  },
  mounted() {
    this.initTreeData();
  },
  methods: {
    // 初始化树节点数据
    initTreeData() {
      this.treeData = [
        {
          title: "卫星底图",
          children: this.layersInMap.filter((e) => e.type === "卫星底图"),
        },
        {
          title: "地图底图",
          children: this.layersInMap.filter((e) => e.type === "地图底图"),
        },
        {
          title: "输出图层",
          children: this.layersInMap.filter((e) => e.type === "输出图层"),
        },
      ];
      this.updateParentChecked();
    },
    // 设置父节点selected,indeterminate,disabled
    updateParentChecked() {
      this.treeData.forEach((e) => {
        let childrenSelectedNum = e.children.filter((e) => e.selected).length;
        if (childrenSelectedNum === 0) {
          e.selected = false;
          e.indeterminate = false;
        } else if (childrenSelectedNum === e.children.length) {
          e.selected = true;
          e.indeterminate = false;
        } else {
          e.indeterminate = true;
        }
        e.disabled = e.children.filter((e) => e.disabled).length?true:false
      });
    },
    // 设置子节点selected
    updateChildrenChecked(data) {
      this.treeData.forEach((e) => {
        if (e.title === data.title) {
          e.children.forEach((i) => {
            i.selected = data.selected;
          });
        }
      });
    },
    // 更新layersIn
    updateLayersIn() {
      this.layersIn = [];
      this.treeData.forEach((e) => {
        this.layersIn.push(...e.children);
      });
      this.$store.commit("SET_LAYERSINMAP", this.layersIn);
    },
  },
  watch: {
    visible(val) {
      if (val){
        this.initTreeData();
      }
    },
    treeData: {
      handler: function () {
        this.updateLayersIn()
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.mapLayerSelection {
  position: fixed;
  top: 40px;
  right: 5px;
  opacity: 0.8;
}
</style>