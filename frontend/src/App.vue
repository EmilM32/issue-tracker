<template>
  <v-app class="background">
    <v-app-bar app color="appBar" dense>
      <v-icon>mdi-jira</v-icon>
      <span class="title pl-5">{{ $appName }}</span>
      <v-spacer />
      <lang-switcher />
      <theme-switcher />
    </v-app-bar>
    <v-main class="ma-5">
      <router-view />
      <base-snackbar />
    </v-main>
  </v-app>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ThemeSwitcher from "@/components/common/ThemeSwitcher.vue";
import LangSwitcher from "@/components/common/LangSwitcher.vue";
import BaseSnackbar from "@/components/common/BaseSnackbar.vue";

@Component({
  components: {
    LangSwitcher,
    ThemeSwitcher,
    BaseSnackbar,
  },
})
export default class App extends Vue {}
</script>
<style lang="sass" scoped>
.background
  background-color: var(--v-background-base)!important
</style>
