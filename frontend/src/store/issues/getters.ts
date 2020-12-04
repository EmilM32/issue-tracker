import { IssuesState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  issuesForProject: (state: IssuesState) => state.issues,
};

const { read } = getStoreAccessors<IssuesState, State>('');

export const readIssues = read(getters.issuesForProject);
