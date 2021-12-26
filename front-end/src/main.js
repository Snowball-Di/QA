import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import live2d from 'ttzxh-vue-live2d'
import live2dcss from '../node_modules/ttzxh-vue-live2d/dist/ttzxh-vue-live2d.css'
import store from './store'
import vueChatScroll from 'vue-chat-scroll'

Vue.config.productionTip = false
Vue.use(live2d)
Vue.use(live2dcss)
Vue.use(vueChatScroll)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
