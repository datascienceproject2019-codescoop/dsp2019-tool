import * as React from 'react'
import styled from '../theme/styled'

interface IProps {
  className?: string
  names: string[]
  distances: number[]
}

class KNNTableClass extends React.PureComponent<IProps> {
  render() {
    const { names, distances } = this.props
    const combined = names.map((n, i) => ({ name: n, distance: distances[i] }))
    return (
      <table className={this.props.className}>
        <thead>
          <tr>
            <th>Owner with name</th>
            <th>Distance</th>
          </tr>
        </thead>
        <tbody>
          { combined.map(c =>
          <tr>
            <td><a href={`https://github.com/${c.name}`} target="__blank">{c.name}</a></td>
            <td>{c.distance}</td>
          </tr>
          )}
        </tbody>
      </table>
    )
  }
}

// const THead = styled.thead`
// `

export const KNNTable = styled(KNNTableClass)``
