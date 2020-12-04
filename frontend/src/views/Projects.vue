<template>
  <div>
    <v-row no-gutters justify="end">
      <v-col style="margin: 1rem 0">
        <span class="title font-weight-regular">
          {{ $tc("projects.title", 2) | capitalize }}
        </span>
      </v-col>
      <v-col cols="3">
        <v-text-field
          v-model="projectSearchModel"
          append-icon="mdi-magnify"
          :label="$t('common.search')"
          single-line
          hide-details
        ></v-text-field>
      </v-col>
    </v-row>
    <v-data-table
      :headers="projectHeaders"
      :items="projects"
      :items-per-page="5"
      :search="projectSearchModel"
      class="elevation-1 mt-5"
      :no-results-text="$t('table.noResultsText')"
      :no-data-text="$t('table.noDataText')"
      :loading-text="$t('table.loadingText')"
      @click:row="goToIssuesPage"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-btn icon @click="showSorting = !showSorting">
            <v-icon> mdi-sort </v-icon>
          </v-btn>
          <v-divider vertical class="mx-2"></v-divider>
          <div v-show="showSorting">
            <v-btn icon @click="sortAscending = !sortAscending">
              <v-icon v-show="sortAscending"> mdi-sort-ascending </v-icon>
              <v-icon v-show="!sortAscending"> mdi-sort-descending </v-icon>
            </v-btn>
            <v-btn text small @click="sortByCreated = !sortByCreated">
              {{ $t(`dates.${sortByCreated ? "createdAt" : "modifiedAt"}`) }}
            </v-btn>
            <v-btn icon color="info" @click="startSorting">
              <v-icon>mdi-check</v-icon>
            </v-btn>
          </div>
          <v-spacer></v-spacer>
          <v-btn
            text
            outlined
            @click="
              selectedProject = undefined;
              projectHandlerModel = true;
            "
            >{{ $t("projects.create") }}</v-btn
          >
          <project-handler
            v-if="projectHandlerModel"
            v-model="projectHandlerModel"
            :selected-project="selectedProject"
          />
        </v-toolbar>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon
          small
          color="info"
          class="mr-2"
          @click.stop="updateProject(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon small color="warning" @click.stop="deleteProject(item)">
          mdi-delete
        </v-icon>
        <confirm-delete
          v-if="confirmDeleteModel"
          v-model="confirmDeleteModel"
          :selected-project="selectedProject"
        />
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { readAllProjects } from "@/store/projects/getters";
import {
  dispatchReadProjects,
  dispatchReadProjectsSorted,
  dispatchSelectProject,
} from "@/store/projects/actions";
import { TranslateResult } from "vue-i18n";
import { Project } from "@/interfaces";
import ProjectHandler from "@/components/projects/ProjectHandler.vue";
import ConfirmDelete from "@/components/projects/ConfirmDelete.vue";

interface ProjectHeader {
  text: TranslateResult;
  value: string;
  sortable?: boolean;
  align?: string;
}

@Component({
  components: {
    ProjectHandler,
    ConfirmDelete,
  },
})
export default class Projects extends Vue {
  private projectHandlerModel = false;
  private confirmDeleteModel = false;
  private selectedProject?: Project;
  private projectSearchModel = "";
  private showSorting = false;
  private sortAscending = true;
  private sortByCreated = true;

  get projectHeaders(): Array<ProjectHeader> {
    return [
      {
        text: this.$t("projects.projId"),
        value: "projId",
      },
      {
        text: this.$t("projects.name"),
        value: "name",
      },
      {
        text: this.$t("common.description"),
        value: "description",
      },
      { text: "Actions", value: "actions", sortable: false, align: "right" },
    ];
  }

  get projects(): Array<Project> {
    return readAllProjects(this.$store);
  }

  async mounted() {
    await dispatchReadProjects(this.$store);
  }

  startSorting(): void {
    dispatchReadProjectsSorted(this.$store, {
      isAsc: this.sortAscending,
      isCreatedAt: this.sortByCreated,
    });
  }

  goToIssuesPage(project: Project): void {
    if (project.id) {
      dispatchSelectProject(this.$store, project);
      this.$router.push({ name: "Issues" });
    }
  }

  deleteProject(project: Project) {
    this.selectedProject = project;
    this.confirmDeleteModel = true;
  }

  updateProject(project: Project) {
    this.selectedProject = project;
    this.projectHandlerModel = true;
  }
}
</script>
