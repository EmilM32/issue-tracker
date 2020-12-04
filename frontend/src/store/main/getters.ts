import { MainState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  firstNotification: (state: MainState) =>
    state.notifications.length > 0 && state.notifications[0],
};

const { read } = getStoreAccessors<MainState, State>('');

export const readFirstNotification = read(getters.firstNotification);
