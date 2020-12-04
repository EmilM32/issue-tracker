import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { IssuesState } from './state';

const defaultState: IssuesState = {
  issues: [],
};

export const issuesModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
