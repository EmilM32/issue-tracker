import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';
import { camelizeKeys, decamelizeKeys } from 'humps';
import { Issue, Project } from '@/interfaces';

const apiUrl = `http://${process.env.VUE_APP_DOMAIN}`;
axios.defaults.baseURL = apiUrl;

// Axios middleware to convert all api responses to camelCase
axios.interceptors.response.use((response: AxiosResponse) => {
  if (
    response.data &&
    response.headers['content-type'] === 'application/json'
  ) {
    response.data = camelizeKeys(response.data);
  }
  return response;
});

// Axios middleware to convert all api requests to snake_case
axios.interceptors.request.use((config: AxiosRequestConfig) => {
  const newConfig = { ...config };
  newConfig.url = config.url;
  if (newConfig.headers['Content-Type'] === 'multipart/form-data')
    return newConfig;
  if (config.params) {
    newConfig.params = decamelizeKeys(config.params);
  }
  if (config.data) {
    newConfig.data = decamelizeKeys(config.data);
  }
  return newConfig;
});

export const api = {
  // api for projects start
  async readProjects(): Promise<Array<Project>> {
    return axios
      .get(`/api/projects/`)
      .then(({ data }) => {
        data.map((el: Project) => {
          if (el.createdAt && el.modifiedAt) {
            el.createdAt = new Date(el.createdAt);
            el.modifiedAt = new Date(el.modifiedAt);
          }
        });
        return data;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },

  async readProjectsSorted(
    isAsc: boolean,
    isCreatedAt: boolean
  ): Promise<Array<Project>> {
    return axios
      .get(`/api/projects/sorted/?is_asc=${isAsc}&is_created_at=${isCreatedAt}`)
      .then(({ data }) => {
        data.map((el: Project) => {
          if (el.createdAt && el.modifiedAt) {
            el.createdAt = new Date(el.createdAt);
            el.modifiedAt = new Date(el.modifiedAt);
          }
        });
        return data;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },

  async createProject(newProject: Project): Promise<Project | number> {
    return axios
      .post(`/api/projects/`, newProject)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((err) => {
        return err.response.status;
      });
  },

  async deleteProject(projId: number): Promise<number> {
    return axios
      .delete(`/api/projects/${projId}`)
      .then((response: AxiosResponse) => {
        return response.data.id;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },

  async updateProject(updateProject: Project): Promise<Project> {
    return axios
      .put(`/api/projects/${updateProject.id}`, updateProject)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },
  // api for projects end

  // api for issues start
  async readIssues(projectId: number): Promise<Array<Issue>> {
    return axios
      .get(`/api/issues/${projectId}`)
      .then(({ data }) => {
        data.map((el: Issue) => {
          if (el.createdAt && el.modifiedAt) {
            el.createdAt = new Date(el.createdAt);
            el.modifiedAt = new Date(el.modifiedAt);
          }
        });

        return data;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },

  async createIssue(newIssue: Issue): Promise<Issue> {
    return axios
      .post(`/api/issues/`, newIssue)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((err) => {
        throw new Error(err.response.status);
      });
  },

  async deleteIssue(issueId: number): Promise<number> {
    return axios
      .delete(`/api/issues/${issueId}`)
      .then((response: AxiosResponse) => {
        return response.data.id;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },

  async updateIssue(updatedIssue: Issue): Promise<Issue> {
    return axios
      .put(`/api/issues/${updatedIssue.id}`, updatedIssue)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((err) => {
        throw new Error(err);
      });
  },
};
