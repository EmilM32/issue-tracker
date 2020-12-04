<template>
  <div>
    <v-snackbar :color="currentNotificationColor" v-model="show">
      {{ $t(currentNotificationContent) }}
      <template v-slot:action="{ attrs }">
        <v-btn icon v-bind="attrs" @click.native="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>
<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { AppNotification } from "@/store/main/state";
import { commitRemoveNotification } from "@/store/main/mutations";
import { readFirstNotification } from "@/store/main/getters";
import { dispatchRemoveNotification } from "@/store/main/actions";

@Component
export default class BaseSnackbar extends Vue {
  public show = false;
  public text = "";
  public currentNotification: AppNotification | false = false;

  public async hide() {
    this.show = false;
    await new Promise<void>((resolve) => setTimeout(() => resolve(), 500));
  }

  public async close() {
    await this.hide();
    await this.removeCurrentNotification();
  }

  public async removeCurrentNotification() {
    if (this.currentNotification) {
      commitRemoveNotification(this.$store, this.currentNotification);
    }
  }

  public get firstNotification() {
    return readFirstNotification(this.$store);
  }

  public async setNotification(notification: AppNotification | false) {
    if (this.show) {
      await this.hide();
    }
    if (notification) {
      this.currentNotification = notification;
      this.show = true;
    } else {
      this.currentNotification = false;
    }
  }

  @Watch("firstNotification")
  public async onNotificationChange(newNotification: AppNotification | false) {
    if (newNotification !== this.currentNotification) {
      await this.setNotification(newNotification);
      if (newNotification) {
        dispatchRemoveNotification(this.$store, {
          notification: newNotification,
          timeout: 6500,
        });
      }
    }
  }

  public get currentNotificationContent() {
    return (this.currentNotification && this.currentNotification.content) || "";
  }

  public get currentNotificationColor() {
    return (
      (this.currentNotification && this.currentNotification.color) || "info"
    );
  }
}
</script>
