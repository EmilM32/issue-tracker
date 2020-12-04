import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { ProjectsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import {
  commitReadProjects,
  commitCreateProject,
  commitDeleteProject,
  commitUpdateProject,
  commitSelectProject,
} from './mutations';
import { Project } from '@/interfaces';
import { commitAddNotification } from '../main/mutations';
import { SnackbarTypes } from '@/enums';

type MainContext = ActionContext<ProjectsState, State>;

export const actions = {
  async actionGetProjects(context: MainContext) {
    const response = await api.readProjects();
    if (response) {
      commitReadProjects(context, response);
    } else {
      commitAddNotification(context, {
        content: 'snackbar.error.blunder',
        color: SnackbarTypes.ERROR,
      });
    }
  },

  async actionGetProjectsSorted(
    context: MainContext,
    sorted: { isAsc: boolean; isCreatedAt: boolean }
  ) {
    const response = await api.readProjectsSorted(
      sorted.isAsc,
      sorted.isCreatedAt
    );
    if (response) {
      commitReadProjects(context, response);
    } else {
      commitAddNotification(context, {
        content: 'snackbar.error.blunder',
        color: SnackbarTypes.ERROR,
      });
    }
  },

  async actionCreateProject(context: MainContext, newProject: Project) {
    const response = await api.createProject(newProject);
    if (response && typeof response !== 'number') {
      commitCreateProject(context, response);
      commitAddNotification(context, {
        content: 'snackbar.success.createProject',
        color: SnackbarTypes.SUCCESS,
      });
    } else if (response === 400) {
      commitAddNotification(context, {
        content: 'snackbar.error.projIdUnique',
        color: SnackbarTypes.ERROR,
      });
    } else {
      commitAddNotification(context, {
        content: 'snackbar.error.blunder',
        color: SnackbarTypes.ERROR,
      });
    }
  },

  async actionDeleteProject(context: MainContext, projId: number) {
    const response = await api.deleteProject(projId);
    if (response) {
      commitDeleteProject(context, response);
      commitAddNotification(context, {
        content: 'snackbar.success.deleteProject',
        color: SnackbarTypes.SUCCESS,
      });
    } else {
      commitAddNotification(context, {
        content: 'snackbar.error.blunder',
        color: SnackbarTypes.ERROR,
      });
    }
  },

  async actionUpdateProject(context: MainContext, updatedProject: Project) {
    const response = await api.updateProject(updatedProject);
    if (response) {
      commitUpdateProject(context, response);
      commitAddNotification(context, {
        content: 'snackbar.success.updateProject',
        color: SnackbarTypes.SUCCESS,
      });
    } else {
      commitAddNotification(context, {
        content: 'snackbar.error.blunder',
        color: SnackbarTypes.ERROR,
      });
    }
  },

  actionSelectProject(context: MainContext, selectedProject: Project) {
    commitSelectProject(context, selectedProject);
  },
};

const { dispatch } = getStoreAccessors<ProjectsState, State>('');

export const dispatchReadProjects = dispatch(actions.actionGetProjects);
export const dispatchReadProjectsSorted = dispatch(
  actions.actionGetProjectsSorted
);
export const dispatchCreateProject = dispatch(actions.actionCreateProject);
export const dispatchDeleteProject = dispatch(actions.actionDeleteProject);
export const dispatchUpdateProject = dispatch(actions.actionUpdateProject);
export const dispatchSelectProject = dispatch(actions.actionSelectProject);
