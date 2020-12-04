import { ProjectsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  allProjects: (state: ProjectsState) => state.projects,

  selectedProject: (state: ProjectsState) => state.selectedProject,
};

const { read } = getStoreAccessors<ProjectsState, State>('');

export const readAllProjects = read(getters.allProjects);
export const getSelectedProject = read(getters.selectedProject);
