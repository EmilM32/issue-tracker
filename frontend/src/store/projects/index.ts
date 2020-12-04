import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { ProjectsState } from './state';

const defaultState: ProjectsState = {
  projects: [],
  selectedProject: undefined,
};

export const projectsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
