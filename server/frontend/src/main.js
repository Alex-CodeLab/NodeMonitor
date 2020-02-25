import Vue from 'vue';
import VueApexCharts from 'vue-apexcharts';
// import VueNativeSock from 'vue-native-websocket';
import App from './App.vue';
import router from './router';


Vue.use(VueApexCharts);
// Vue.use(VueNativeSock, 'ws://localhost:5555', { protocol: 'pub.sp.nanomsg.org', reconnection: true });
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
