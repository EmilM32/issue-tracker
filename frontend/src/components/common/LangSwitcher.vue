<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-web</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item dense>
        <v-list-item-title>
          <v-btn
            v-for="lang in languages"
            :key="lang"
            icon
            @click="changeLang(lang)"
          >
            <img :src="`/flags/${lang}.svg`" width="25" :alt="lang" />
          </v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

interface LangSwitcherTemplate {
  languages: Array<string>;
  changeLang(lang: string): void;
}

@Component
export default class LangSwitcher extends Vue implements LangSwitcherTemplate {
  languages = ["en", "pl"];

  changeLang(lang: string): void {
    this.$i18n.locale = lang;
  }
}
</script>
