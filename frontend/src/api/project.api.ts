import {
  get,
  post,
} from './methods'

import { IProject } from 'src/types/project'

export const getProjects = () =>
  get<IProject[]>('projects')

export const predictStars = (nameWithOwner: string) =>
  post<IProject>('projects/predict', { nameWithOwner })
