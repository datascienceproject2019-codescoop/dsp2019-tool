export interface IProject {
  'BSD-2-Clause': string // boolean
  CSS: string // boolean
  'Contributors Count': number
  'Created Timestamp': string // "2015-01-15 02:20:32 UTC"
  'Default branch': string // boolean
  Description: string // "Silvertripe side bar menu widget"
  'Emacs Lisp': string // boolean
  Fork: string // boolean
  'Forks Count': number
  Go: string // boolean
  HTML: string // boolean
  'Homepage URL': string
  'Issues enabled': string // boolean
  Java: string // boolean
  JavaScript: string // boolean
  'Last pushed Timestamp': string // "2016-09-29 00:32:12 UTC"
  MIT: string // boolean
  'Name with Owner': string // "guru-digital/silverstripe-widget-sidebar-nav"
  'Objective-C': string // boolean
  'Open Issues Count': string // boolean
  Other: string // boolean
  PHP: string // boolean
  'Pages enabled': string // boolean
  'Pull requests enabled': string // boolean
  Python: string // boolean
  Scala: string // boolean
  Shell: string // boolean
  Size: number
  SourceRank: number
  'Updated Timestamp': string // "2017-10-07 21:31:49 UTC"
  'Watchers Count': number
  'Wiki enabled': string // boolean
  Language: string
  Keywords: string
  'Stars Count': number
}

export interface IProjectPredicted extends IProject {
  predicted_stars: number
  knn_names: string[]
  knn_distances: number[]
}
