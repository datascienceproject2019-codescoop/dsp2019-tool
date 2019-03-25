import { IProject } from '../types/project'

import {
  get,
} from './methods'

export const getProjects = () =>
  get<{users: IProject[]}>('projects')
