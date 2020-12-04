import { Project } from '@/interfaces';

export interface ProjectsState {
  projects: Array<Project>;
  selectedProject?: Project;
}
