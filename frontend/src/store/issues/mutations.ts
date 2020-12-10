import { IssuesState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { Issue } from '@/interfaces';

export const mutations = {
  readIssues(state: IssuesState, payload: Array<Issue>) {
    state.issues = payload;
  },

  createIssue(state: IssuesState, payload: Issue) {
    state.issues.push(payload);
  },

  deleteIssue(state: IssuesState, payload: number) {
    const issues = state.issues.filter((value) => {
      return value.id !== payload;
    });

    state.issues = issues;
  },

  updateIssue(state: IssuesState, payload: Issue) {
    const issues = state.issues.filter((value) => {
      return value.id !== payload.id;
    });
    state.issues = issues;
    state.issues.push(payload);
  },
};

const { commit } = getStoreAccessors<IssuesState, State>('');

export const commitReadIssues = commit(mutations.readIssues);
export const commitCreateIssue = commit(mutations.createIssue);
export const commitDeleteIssue = commit(mutations.deleteIssue);
export const commitUpdateIssue = commit(mutations.updateIssue);
