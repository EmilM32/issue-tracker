import { IssueStatus } from '@/enums';

export interface Project {
  id?: number;
  projId: string;
  name: string;
  description: string;
  createdAt?: Date;
  modifiedAt?: Date;
}

export interface Issue {
  id?: number;
  summary: string;
  description: string;
  status: IssueStatus;
  projId: number;
  issueId: string;
  createdAt?: Date;
  modifiedAt?: Date;
  issuesRelations?: Array<Issue>;
}
