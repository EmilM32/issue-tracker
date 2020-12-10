import Vue from 'vue';

export default function() {
  Vue.filter('capitalize', function(value: string) {
    if (!value) return '';
    return value.charAt(0).toUpperCase() + value.slice(1);
  });
}
