import Vue from 'vue';
import vuetify from './plugins/vuetify';
import App from './App.vue';
import router from './router';
import store from '@/store';
import i18n from './plugins/i18n';
import filters from './plugins/filters';
import vueKanban from 'vue-kanban';

Vue.prototype.$appName = 'Issue Tracker';

Vue.config.productionTip = false;

Vue.use(filters);
Vue.use(vueKanban);

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount('#app');
