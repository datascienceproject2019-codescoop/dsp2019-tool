import { action, runInAction, observable } from 'mobx'
import * as projectApi from '../api/project.api'

import { IProject } from '../types/project'

export class ProjectStore {
  @observable projects: IProject[] = []
  @observable loading = false

  @action
  getProjects = async () => {
    this.loading = true
    const result = await projectApi.getProjects() as IProject[]
    return runInAction(() => {
      this.projects = result
      this.loading = false
      return result
    })
  }

  predictStars = async (nameWithOwner: string) => {
    this.loading = true
    const result = await projectApi.predictStars(nameWithOwner)
    return runInAction(() => {
      this.loading = false
      return result
    })
  }
}
