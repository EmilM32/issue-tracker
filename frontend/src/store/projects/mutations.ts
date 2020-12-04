import { ProjectsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { Project } from '@/interfaces';

export const mutations = {
  readProjects(state: ProjectsState, payload: Array<Project>) {
    state.projects = payload;
  },

  createProject(state: ProjectsState, payload: Project) {
    state.projects.push(payload);
  },

  deleteProject(state: ProjectsState, payload: number) {
    const projects = state.projects.filter((value) => {
      return value.id !== payload;
    });
    state.projects = projects;
  },

  updateProject(state: ProjectsState, payload: Project) {
    const projects = state.projects.filter((value) => {
      return value.id !== payload.id;
    });
    state.projects = projects;
    state.projects.push(payload);
  },

  selectProject(state: ProjectsState, payload: Project) {
    state.selectedProject = payload;
  },
};

const { commit } = getStoreAccessors<ProjectsState, State>('');

export const commitReadProjects = commit(mutations.readProjects);
export const commitCreateProject = commit(mutations.createProject);
export const commitDeleteProject = commit(mutations.deleteProject);
export const commitUpdateProject = commit(mutations.updateProject);
export const commitSelectProject = commit(mutations.selectProject);
