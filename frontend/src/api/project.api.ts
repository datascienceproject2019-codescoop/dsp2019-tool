import { parse } from 'papaparse'

// import {
//   get,
// } from './methods'

export const getProjects = () => {
  return new Promise((resolve, reject) => {
    parse(require('./data500.csv'), {
      delimiter: ',',
      download: true,
      header: true,
      skipEmptyLines: true,
      complete(results) {
        resolve(results.data.map((r) => {
          // for (const key in r) {
          //   r[key] = parseInt(r[key])
          // }
          return r
        }))
      },
      error(err) {
        reject(err)
      }
    })
  })
}
