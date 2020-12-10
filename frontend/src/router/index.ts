import Vue from 'vue';
import Router from 'vue-router';

import Projects from '@/views/Projects.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Projects',
      component: Projects,
    },
    {
      path: '/issues',
      name: 'Issues',
      component: () => import('@/views/Issues.vue'),
    },
    {
      path: '/*',
      redirect: '/',
    },
  ],
});
