<template>
  <v-dialog v-model="confirmDeleteModel" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        {{ $t("projects.delete") | capitalize }}
      </v-card-title>
      <v-card-text>
        {{
          $tc("projects.deleteConfirmMsg", 1, { key: selectedProject.projId })
        }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn icon color="warning" @click="deleteProject(selectedProject.id)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
        <v-btn icon @click="$emit('input', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { SnackbarTypes } from "@/enums";
import { Project } from "@/interfaces";
import { dispatchAddNotification } from "@/store/main/actions";
import { AppNotification } from "@/store/main/state";
import { dispatchDeleteProject } from "@/store/projects/actions";
import { Component, Vue, Model, Prop } from "vue-property-decorator";

@Component
export default class ConfirmDelete extends Vue {
  @Model("input") confirmDeleteModel!: boolean;
  @Prop() selectedProject?: Project;

  mounted() {
    if (!this.selectedProject?.id) {
      const snackbar: AppNotification = {
        content: "snackbar.error.blunder",
        color: SnackbarTypes.ERROR,
      };
      dispatchAddNotification(this.$store, snackbar);
      this.$emit("input", false);
    }
  }

  async deleteProject(id: number) {
    await dispatchDeleteProject(this.$store, id);
    this.$emit("input", false);
  }
}
</script>
