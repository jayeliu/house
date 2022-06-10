import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import installElementPlus from './plugins/element'

// 样式表
import './assets/css/global.css'
// 全局指令
import divDrag from "@/myDirectives/divDrag.js"

const app = createApp(App)
installElementPlus(app)
app.use(store).use(router).directive("divDrag", divDrag).mount('#app')