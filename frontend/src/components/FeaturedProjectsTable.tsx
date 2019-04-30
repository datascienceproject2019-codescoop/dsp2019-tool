import * as React from 'react'
import styled from '../theme/styled'
import { Link } from 'react-router-dom'

import { IProject } from 'src/types/project'

interface IProps {
  className?: string
  projects: IProject[]
  shownProjects: boolean[]
}

class FeaturedProjectsTableClass extends React.PureComponent<IProps> {
  render() {
    const { projects, shownProjects } = this.props
    console.log('render')
    return (
      <table className={this.props.className}>
        <thead>
          <tr>
            <th>Rating</th>
            <th>Stars</th>
            <th>Language</th>
            <th>Owner/name</th>
          </tr>
        </thead>
        <tbody>
          { projects.map((p, i) =>
          <Row key={p['Name with Owner']} className={shownProjects[i] ? '' : 'hidden'}>
            <td>{p['Rating']}</td>
            <td>{p['Stars Count']}</td>
            <td>{p['Language']}</td>
            <td><Link to={`projects/${p['Name with Owner']}`}>{p['Name with Owner']}</Link></td>
          </Row>
          )}
        </tbody>
      </table>
    )
  }
}

const Row = styled.tr`
  margin: 5px;
  &.hidden {
    visibility: hidden;
    display: none;
  }
`

export const FeaturedProjectsTable = styled(FeaturedProjectsTableClass)``
