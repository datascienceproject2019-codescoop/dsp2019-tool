import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { RouteComponentProps } from 'react-router'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
// import { IProject } from '../types/project'

interface IProps extends RouteComponentProps<{ownerName: string, projectName: string}> {
  projecStore?: ProjectStore,
}

@inject((stores: Stores) => ({
  projecStore: stores.projectStore,
}))
@observer
export class ProjectPage extends React.Component<IProps> {
  componentDidMount() {
    this.props.projecStore!.getProjects()
  }
  render() {
    const { ownerName, projectName } = this.props.match.params
    return (
      <Container>
        <header>
          <h1>{ownerName}/{projectName}</h1>
        </header>
        <p>Is a cool project</p>
        <div>
          <p>something</p>
        </div>
      </Container>
    )
  }
}

const Container = styled.div`
`
// const UsersList = styled.ul`
// `
// const UsersListItem = styled.li`
//   display: flex;
//   flex-direction: column;
//   margin: 0 0 10px 0;
//   & > p {
//     margin: 0 10px 0 0;
//   }
// `
