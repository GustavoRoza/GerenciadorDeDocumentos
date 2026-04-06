import { createRouter, createWebHistory } from 'vue-router'


import UploadTeste from './components/UploadTeste.vue'
import DashboardPrincipal from './components/DashboardPrincipal.vue' 


const rotas = [
  { path: '/', component: DashboardPrincipal },
  { path: '/upload', component: UploadTeste }
]


const roteador = createRouter({
  history: createWebHistory(),
  routes: rotas
})


export default roteador