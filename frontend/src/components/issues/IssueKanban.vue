<template>
  <div>
    <v-row justify="center">
      <v-btn
        v-for="status in [
          IssueStatus.TODO,
          IssueStatus.IN_PROGRESS,
          IssueStatus.DONE,
        ]"
        :key="status"
        small
        outlined
        text
        :color="!availableStatuses.includes(status) ? 'grey darken-1' : ''"
        @click="toggleBlock(status)"
        >{{ $t(`issues.statuses.${status}`) }}</v-btn
      >
    </v-row>
    <kanban-board
      :stages="availableStatuses"
      :blocks="issues"
      :config="config"
      @update-block="updateBlock"
    >
      <div v-for="status in availableStatuses" :slot="status" :key="status">
        <h2>
          {{ $t(`issues.statuses.${status}`) }}
          {{ issuesCount(status) }}
        </h2>
      </div>
      <v-card
        v-for="issue in issues"
        :slot="issue.id"
        :key="issue.id"
        min-height="70"
        @click="$emit('show-issue-details', issue)"
        v-show="
          issue.issueId.toLowerCase().includes(searchModel) ||
          issue.summary.toLowerCase().includes(searchModel)
        "
      >
        <p class="pa-2">{{ issue.summary }}</p>
        <p class="text-right pa-2">
          {{ issue.issueId }}
        </p>
      </v-card>
    </kanban-board>
  </div>
</template>

<script lang="ts">
import { IssueStatus } from "@/enums";
import { Issue } from "@/interfaces";
import { dispatchUpdateIssue } from "@/store/issues/actions";
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class IssueKanban extends Vue {
  @Prop({ required: true }) issues!: Array<Issue>;
  @Prop({ required: true }) searchModel!: string;
  IssueStatus = IssueStatus;
  availableStatuses: Array<IssueStatus> = [
    IssueStatus.TODO,
    IssueStatus.IN_PROGRESS,
    IssueStatus.DONE,
  ];

  config = {
    // Don't allow blocks to be moved out of the approved stage
    accepts: (block: HTMLElement, target: HTMLElement, source: HTMLElement) => {
      const currentStatus = source.dataset.status;
      const targetStatus = target.dataset.status;
      const allowedStatus = this.statusChangeFlow(currentStatus as IssueStatus);

      return targetStatus === allowedStatus;
    },
  };

  statusChangeFlow(currentStatus: IssueStatus): IssueStatus | boolean {
    switch (currentStatus) {
      case IssueStatus.TODO:
        return IssueStatus.IN_PROGRESS;
        break;
      case IssueStatus.IN_PROGRESS:
        return IssueStatus.DONE;
        break;
      case IssueStatus.DONE:
        return false;
        break;
      default:
        console.warn(`unknown status ${currentStatus}`);
        return false;
    }
  }

  toggleBlock(status: IssueStatus): void {
    if (!this.availableStatuses.includes(status)) {
      this.availableStatuses.push(status);
    } else {
      this.availableStatuses = this.availableStatuses.filter((el) => {
        return el !== status;
      });
    }
    const orderMap = { TODO: 1, IN_PROGRESS: 2, DONE: 3 };
    this.availableStatuses.sort(function(x, y) {
      return orderMap[x] - orderMap[y];
    });
  }

  issuesCount(status: IssueStatus): number {
    return this.issues.reduce(
      (count, issue) => count + Number(issue.status === status),
      0
    );
  }

  updateBlock(id: string, status: string): void {
    const updatedIssue = this.issues.find((issue) => {
      return issue.id === Number(id);
    });
    if (updatedIssue) {
      updatedIssue.status = status as IssueStatus;

      dispatchUpdateIssue(this.$store, updatedIssue);
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/kanban.scss";
</style>