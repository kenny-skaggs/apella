import './my.sass'
import "@fortawesome/fontawesome-free/css/all.css"

import Vue from 'vue'
import Buefy from 'buefy'
import '@fortawesome/fontawesome-free'

import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App.vue'
import router from './router'
import store from './store'

import ioClient from 'socket.io-client';
import VueSocketIO from "vue-socket.io";

Vue.use(Buefy)

axios.defaults.headers['Access-Control-Allow-Origin'] = '*'
axios.defaults.baseURL = 'http://localhost:5000'
Vue.use(VueAxios, axios)

Vue.config.productionTip = false


const connectionOptions = {
  connection: ioClient('http://localhost:5000', {
    cors: {
      origin: '*'
    },
    extraHeaders: {
      Authorization: 'Bearer' + store.state.authToken
    }
  }),
  debug: true
}
Vue.use(new VueSocketIO(connectionOptions));

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
