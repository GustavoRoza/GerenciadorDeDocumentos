import { createApp } from 'vue'
import App from './App.vue'
import roteador from './router.js' 

const app = createApp(App)

app.use(roteador) 

app.mount('#app')