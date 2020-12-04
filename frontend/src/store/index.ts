import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { mainModule } from './main';
import { State } from './state';
import { projectsModule } from './projects';
import { issuesModule } from './issues';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    projects: projectsModule,
    issues: issuesModule,
    main: mainModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
