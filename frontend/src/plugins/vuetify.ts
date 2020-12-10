import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    options: { customProperties: true },
    themes: {
      light: {
        appBar: '#00A9B7',
        background: '#F2F2F2',
      },
      dark: {
        appBar: colors.cyan.darken4,
        background: '#1D2021',
      },
    },
  },
});
