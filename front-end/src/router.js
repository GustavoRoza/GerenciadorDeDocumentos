import { createRouter, createWebHistory } from 'vue-router'

// 1. Importamos todas as 3 telas do nosso sistema
import TelaLogin from './components/TelaLogin.vue'
import DashboardPrincipal from './components/DashboardPrincipal.vue'
import UploadTeste from './components/UploadTeste.vue'

// 2. Reorganizamos as rotas
const rotas = [
  { path: '/', component: TelaLogin }, // O caminho raiz agora é o Login
  { path: '/dashboard', component: DashboardPrincipal }, // O Dashboard ganhou um novo endereço
  { path: '/upload', component: UploadTeste }
]

// 3. Ligamos o roteador
const roteador = createRouter({
  history: createWebHistory(),
  routes: rotas
})

export default roteador