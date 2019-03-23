import { action, runInAction, observable } from 'mobx'
import * as projectApi from '../api/project.api'

import { IProject } from '../types/project'

export class ProjectStore {
  @observable projects: IProject[] = []
  @observable loading = false

  @action
  getProjects = async () => {
    this.loading = true
    const result = await projectApi.getProjects()
    runInAction(() => {
      this.projects = result.users
      this.loading = false
    })
  }
}
