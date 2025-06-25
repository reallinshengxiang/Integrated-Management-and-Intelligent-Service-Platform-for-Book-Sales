import { createApp } from 'vue'
import store from './store'
import ElementPlus from "element-plus"
import 'element-plus/dist/index.css'
import router from './router/index'
import './style.css'
import App from './App.vue'

createApp(App).use(ElementPlus).use(router).use(store).mount('#app')
