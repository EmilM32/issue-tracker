<template>
  <v-dialog v-model="issueDetailsModel" max-width="700px" persistent>
    <v-card>
      <v-card-title>
        <span v-if="issue">
          {{ $tc("issues.title", 1) | capitalize }} {{ issueData.issueId }}
        </span>
        <span v-else>
          {{ $t("issues.create") | capitalize }}
        </span>
        <v-spacer />
        <v-btn
          v-if="issue && issueData.status !== IssueStatus.DONE"
          icon
          small
          :color="isReadonly ? 'grey' : 'blue darken-4'"
          @click="isReadonly = !isReadonly"
        >
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn
          v-if="issue"
          icon
          small
          color="warning"
          @click="deleteIssue(issue.id)"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-form ref="issueForm">
          <v-row dense>
            <v-col cols="12">
              <v-textarea
                v-model="issueData.summary"
                dense
                outlined
                counter="50"
                :label="$t('issues.summary')"
                :rules="rules.summary"
                required
                :readonly="isReadonly"
                height="60"
              ></v-textarea>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="issueData.description"
                dense
                outlined
                counter="150"
                :label="$t('common.description')"
                :rules="rules.description"
                :readonly="isReadonly"
                required
                height="150"
              ></v-textarea>
            </v-col>
            <v-col cols="12">
              <v-autocomplete
                v-model="issueData.issuesRelations"
                :items="issue ? filteredIssuesForProject() : issuesForProject"
                :menu-props="{ maxHeight: '400' }"
                :label="$t('issues.relations')"
                dense
                outlined
                return-object
                item-text="issueId"
                item-value="id"
                multiple
                persistent-hint
                :readonly="isReadonly"
              >
              </v-autocomplete>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn v-if="!isReadonly" icon color="success" @click="saveData">
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
import { IssueStatus, SnackbarTypes } from "@/enums";
import { Issue, Project } from "@/interfaces";
import {
  dispatchCreateIssues,
  dispatchDeleteIssues,
  dispatchUpdateIssue,
} from "@/store/issues/actions";
import { dispatchAddNotification } from "@/store/main/actions";
import { AppNotification } from "@/store/main/state";
import { getSelectedProject } from "@/store/projects/getters";
import { VForm } from "@/types";
import { TranslateResult } from "vue-i18n";
import { Component, Vue, Model, Prop, Ref } from "vue-property-decorator";

@Component
export default class IssueDetails extends Vue {
  @Model("input") issueDetailsModel!: boolean;
  @Prop({ required: false }) issue?: Issue;
  @Prop({ required: true }) issuesForProject!: Array<Issue>;
  @Ref("issueForm") readonly issueForm!: VForm;

  private isReadonly = false;

  private issueData: Issue = {
    summary: "",
    description: "",
    status: IssueStatus.TODO,
    projId: this.selectedProject?.id || -1,
    issueId: this.selectedProject?.projId || "",
    issuesRelations: [],
  };

  private rules = {
    summary: [this.checkRequired, this.summaryLenght],
    description: [this.checkRequired, this.descriptionLenght],
  };

  private IssueStatus = IssueStatus;

  mounted() {
    if (this.issue) {
      this.issueData = JSON.parse(JSON.stringify(this.issue));
      this.isReadonly = true;
    }
  }


  get selectedProject(): Project | undefined {
    return getSelectedProject(this.$store);
  }

  checkRequired(val: string): boolean | TranslateResult {
    return !!val || this.$t("rules.required");
  }

  summaryLenght(val: string): boolean | TranslateResult {
    return val.length <= 50 || this.$t("rules.tooLong");
  }

  descriptionLenght(val: string): boolean | TranslateResult {
    return val.length <= 150 || this.$t("rules.tooLong");
  }

  deleteIssue(issueId: number): void {
    dispatchDeleteIssues(this.$store, issueId);
    this.$emit("input", false);
  }

  filteredIssuesForProject(): Array<Issue> {
    return this.issuesForProject.filter((issue) => {
      return issue.issueId !== this.issueData.issueId;
    });
  }

  async saveData(): Promise<void> {
    if (this.issueForm.validate()) {
      if (this.issue) {
        dispatchUpdateIssue(this.$store, this.issueData);
      } else {
        dispatchCreateIssues(this.$store, this.issueData);
      }
      this.issueForm.resetValidation();
      this.$emit("input", false);
    } else {
      const snackbar: AppNotification = {
        content: "snackbar.error.formValid",
        color: SnackbarTypes.ERROR,
      };
      dispatchAddNotification(this.$store, snackbar);
    }
  }
}
</script>
