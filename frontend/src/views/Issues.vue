<template>
  <div style="margin: 1rem">
    <v-row justify="space-between">
      <v-col cols="12" md="4">
        <v-btn icon class="mr-5" @click="$router.go(-1)">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <span class="title font-weight-regular">
          {{ selectedProject.name }} /
          {{ $tc("issues.title", 2) | capitalize }}
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model="issueSearchModel"
          append-icon="mdi-magnify"
          :label="$t('common.search')"
          single-line
          hide-details
          style="padding-top: 0; margin-top: 0"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="4" align="end">
        <v-btn text outlined @click="showIssueDetails(undefined)">{{
          $t("issues.create")
        }}</v-btn>
      </v-col>
    </v-row>
    <issue-kanban
      v-if="issuesForProject"
      :issues="issuesForProject"
      :search-model="issueSearchModel"
      @show-issue-details="showIssueDetails"
    />
    <issue-details
      v-if="issueDetailsModel"
      v-model="issueDetailsModel"
      :issue="selectedIssue"
      :issues-for-project="issuesForProject"
    />
  </div>
</template>

<script lang="ts">
import { IssueStatus } from "@/enums";
import { Issue, Project } from "@/interfaces";
import { dispatchReadIssues } from "@/store/issues/actions";
import { readIssues } from "@/store/issues/getters";
import { Component, Vue } from "vue-property-decorator";
import IssueKanban from "@/components/issues/IssueKanban.vue";
import IssueDetails from "@/components/issues/IssueDetails.vue";
import { getSelectedProject } from "@/store/projects/getters";

@Component({
  components: { IssueKanban, IssueDetails },
})
export default class Issues extends Vue {
  private issueDetailsModel = false;
  private selectedIssue?: Issue;
  private issueSearchModel = "";

  get selectedProject(): Project | undefined {
    return getSelectedProject(this.$store);
  }

   get issuesForProject(): Array<Issue> {
    return readIssues(this.$store);
  }

  showIssueDetails(issue: Issue | undefined): void {
    this.selectedIssue = issue;
    this.issueDetailsModel = true;
  }

  mounted() {
    if (this.selectedProject?.id) {
      dispatchReadIssues(this.$store, this.selectedProject.id);
    } else {
      this.$router.go(-1);
    }
  }
}
</script>