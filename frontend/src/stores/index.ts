import { ProjectStore } from './ProjectStore'

export class Stores {
  public projectStore: ProjectStore

  constructor() {
    this.projectStore = new ProjectStore()
  }
}
