import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { IssuesState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import {
  commitReadIssues,
  commitCreateIssue,
  commitDeleteIssue,
  commitUpdateIssue,
} from './mutations';
import { Issue } from '@/interfaces';

type MainContext = ActionContext<IssuesState, State>;

export const actions = {
  async actionReadIssues(context: MainContext, projectId: number) {
    const response = await api.readIssues(projectId);
    if (response) {
      commitReadIssues(context, response);
    }
  },

  async actionCreateIssue(context: MainContext, newIssue: Issue) {
    const response = await api.createIssue(newIssue);
    if (response) {
      commitCreateIssue(context, response);
    }
  },

  async actionDeleteIssue(context: MainContext, issueId: number) {
    const response = await api.deleteIssue(issueId);
    if (response) {
      commitDeleteIssue(context, response);
    }
  },

  async actionUpdateIssue(context: MainContext, updatedIssue: Issue) {
    const response = await api.updateIssue(updatedIssue);
    if (response) {
      commitUpdateIssue(context, response);
    }
  },
};

const { dispatch } = getStoreAccessors<IssuesState, State>('');

export const dispatchReadIssues = dispatch(actions.actionReadIssues);
export const dispatchCreateIssues = dispatch(actions.actionCreateIssue);
export const dispatchDeleteIssues = dispatch(actions.actionDeleteIssue);
export const dispatchUpdateIssue = dispatch(actions.actionUpdateIssue);
