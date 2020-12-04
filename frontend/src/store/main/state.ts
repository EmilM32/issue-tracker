export interface AppNotification {
  content: string;
  color: string;
}

export interface MainState {
  notifications: AppNotification[];
}
