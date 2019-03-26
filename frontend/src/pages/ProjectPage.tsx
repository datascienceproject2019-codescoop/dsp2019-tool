import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { RouteComponentProps } from 'react-router'

import { LineChart } from '../components/Charts'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
import { IProject } from '../types/project'

interface IProps extends RouteComponentProps<{ownerName: string, projectName: string}> {
  projecStore?: ProjectStore,
}
interface IState {
  thisProject?: IProject
}

@inject((stores: Stores) => ({
  projecStore: stores.projectStore,
}))
@observer
export class ProjectPage extends React.Component<IProps, IState> {
  state = {
    thisProject: undefined
  }
  componentDidMount() {
    this.props.projecStore!.getProjects()
  }
  render() {
    const { ownerName, projectName } = this.props.match.params
    const tp = this.props.projecStore!.projects.find(
      p => p['Name with Owner'] === `${ownerName}/${projectName}`)
    return (
      <Container>
        { tp === undefined ? 'loading' :
        <div>
          <h1>{ownerName}/{projectName}</h1>
          <p>{tp!.Description}</p>
          <div>
            <AttributesList>
              <AttributesListItem>Stars Count: {tp!['Stars Count']}</AttributesListItem>
              <AttributesListItem>Language: {tp!['Language']}</AttributesListItem>
              <AttributesListItem>Forks Count: {tp!['Forks Count']}</AttributesListItem>
            </AttributesList>
          </div>
          <ChartContainer>
            <h2>Graph for commits and stars</h2>
            <LineChart />
          </ChartContainer>
        </div>
        }
      </Container>
    )
  }
}

const Container = styled.div`
`
const AttributesList = styled.ul`
`
const AttributesListItem = styled.li`
  display: flex;
  flex-direction: column;
  margin: 0 0 10px 0;
  & > p {
    margin: 0 10px 0 0;
  }
`
const ChartContainer = styled.div`
  margin: 20px 0 0 0;
`
