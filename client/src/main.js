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
import VueSocketIO from "vue-socket.io-extended";

import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';

let socket_server_url = undefined;
if (process.env.NODE_ENV === 'production') {
    Sentry.init({
        dsn: 'https://dae90bfc53404a8bb51befc5550b7ebf@app.glitchtip.com/1289',
        integrations: [new Integrations.Vue({ Vue })]
    });
    socket_server_url = window.location;
} else {
    axios.defaults.headers['Access-Control-Allow-Origin'] = '*'
    axios.defaults.baseURL = 'http://localhost:5000'
    socket_server_url = 'http://localhost:5000'
}

Vue.use(Buefy)

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

Vue.use(VueSocketIO, ioClient(socket_server_url, {
    cors: {
        origin: '*'
    },
    autoConnect: false
}));

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
