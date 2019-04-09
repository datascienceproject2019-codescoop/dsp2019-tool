import {
  get,
  post,
} from './methods'

import { IProject, IProjectPredicted } from 'src/types/project'

export const getProjects = () =>
  get<IProject[]>('projects')

export const predictStars = (nameWithOwner: string) =>
  post<IProjectPredicted>('projects/predict', { nameWithOwner })
