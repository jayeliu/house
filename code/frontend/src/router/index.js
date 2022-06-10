import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    redirect: '/tableView'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/login',
    name: 'loginDialog',
    component: () => import('@/views/loginDialog')
  },
  {
    path: '/tableView',
    name: 'TableView',
    component: () => import('@/views/tableView')
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import('@/views/map')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
