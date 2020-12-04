import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { commitAddNotification, commitRemoveNotification } from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
  actionAddNotification(context: MainContext, snackbar: AppNotification) {
    commitAddNotification(context, snackbar);
  },

  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number }
  ) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchAddNotification = dispatch(actions.actionAddNotification);
