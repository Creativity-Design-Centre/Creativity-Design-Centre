import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import axios from 'axios'
import VueDragResize from 'vue-drag-resize'
import 'ant-design-vue/dist/antd.css'

Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.use(Antd)

Vue.component('vue-drag-resize', VueDragResize)

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app')
