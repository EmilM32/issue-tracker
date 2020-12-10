<template>
  <v-dialog v-model="projectHandlerModel" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        {{
          $t(`projects.${selectedProject ? "update" : "create"}`) | capitalize
        }}
      </v-card-title>
      <v-card-text>
        <v-form ref="currentProjectForm">
          <v-row dense>
            <v-col cols="6">
              <v-text-field
                v-model="projectData.projId"
                dense
                outlined
                counter="8"
                :label="$t('projects.projId')"
                :rules="rules.projId"
                required
                :disabled="!!selectedProject"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="projectData.name"
                dense
                outlined
                :label="$t('projects.name')"
                counter="15"
                :rules="rules.name"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                outlined
                :label="$t('common.description')"
                v-model="projectData.description"
                :rules="rules.description"
                required
                counter="150"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn icon color="success" @click="saveData">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
        <v-btn icon @click="$emit('input', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Ref, Model, Prop } from "vue-property-decorator";
import { Project } from "@/interfaces";
import {
  dispatchCreateProject,
  dispatchUpdateProject,
} from "@/store/projects/actions";
import { TranslateResult } from "vue-i18n";
import { VForm } from "@/types";

@Component
export default class ProjectHandler extends Vue {
  @Model("input") projectHandlerModel!: boolean;
  @Ref("currentProjectForm") readonly currentProjectForm!: VForm;
  @Prop({ required: false }) selectedProject?: Project;

  private projectData: Project = {
    name: "",
    description: "",
    projId: "",
  };

  private rules = {
    projId: [this.checkRequired, this.projIdLenght],
    name: [this.checkRequired, this.projNameLenght],
    description: [this.checkRequired, this.projDescriptionLenght],
  };

  mounted() {
    if (this.selectedProject) {
      this.projectData = JSON.parse(JSON.stringify(this.selectedProject));
    }
  }

  checkRequired(val: string): boolean | TranslateResult {
    return !!val || this.$t("rules.required");
  }

  projIdLenght(val: string): boolean | TranslateResult {
    return val.length <= 8 || this.$t("rules.tooLong");
  }

  projNameLenght(val: string): boolean | TranslateResult {
    return val.length <= 15 || this.$t("rules.tooLong");
  }

  projDescriptionLenght(val: string): boolean | TranslateResult {
    return val.length <= 150 || this.$t("rules.tooLong");
  }

  async saveData(): Promise<void> {
    if (this.currentProjectForm.validate()) {
      if (this.selectedProject) {
        await dispatchUpdateProject(this.$store, this.projectData);
      } else {
        await dispatchCreateProject(this.$store, this.projectData);
      }
      this.currentProjectForm.resetValidation();
      this.$emit("input", false);
    }
  }
}
</script>
