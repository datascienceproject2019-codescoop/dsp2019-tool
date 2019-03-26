import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { RouteComponentProps } from 'react-router'
import {
  GoStar,
  GoRepoForked,
  GoIssueOpened,
  GoFileCode
} from 'react-icons/go'

import { LineChart } from '../components/Charts'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
import { IProject } from '../types/project'
import { StyledComponentClass } from 'styled-components'
import { ITheme } from '../types/theme'

interface IProps extends RouteComponentProps<{ownerName: string, projectName: string}> {
  projecStore?: ProjectStore,
}
interface IState {
  loading: boolean
  error?: string
  fetchedProject?: IProject
}

@inject((stores: Stores) => ({
  projecStore: stores.projectStore,
}))
@observer
export class ProjectPage extends React.Component<IProps, IState> {
  state: IState = {
    loading: true,
    error: undefined,
    fetchedProject: undefined
  }
  async componentDidMount() {
    const { ownerName, projectName } = this.props.match.params
    this.setState({ loading: true })
    const result = await this.props.projecStore!.predictStars(`${ownerName}/${projectName}`)
    if (result) {
      this.setState({
        loading: false,
        fetchedProject: result,
      })
    } else {
      this.setState({
        loading: false,
        error: 'Unable to get the project from the API. I AM SORRY.'
      })
    }
  }
  render() {
    const { ownerName, projectName } = this.props.match.params
    const { loading, error } = this.state
    const p = this.state.fetchedProject
    return (
      <Container>
        { loading ? 'loading' : error ? error :
        <div>
          <TopContainer>
            <h1>{ownerName}/{projectName}</h1>
            <div>
              <AttributesList>
                <AttributesListItem color="yellow">
                  <GoStar size={24}/>
                  <span>{p!['Stars Count']}</span>
                </AttributesListItem>
                <AttributesListItem color="lightgrey">
                  <GoFileCode size={24}/>
                  <span>{p!['Language']}</span>
                </AttributesListItem>
                <AttributesListItem color="green">
                  <GoRepoForked size={24}/>
                  <span>{p!['Forks Count']}</span>
                </AttributesListItem>
                <AttributesListItem color="orange">
                  <GoIssueOpened size={24}/>
                  <span>{p!['Open Issues Count']}</span>
                </AttributesListItem>
              </AttributesList>
            </div>
            <p><i>{p!.Description}</i></p>
          </TopContainer>
          <PredictedContainer>
            <h2>Predicted stars: </h2>
            <b>{p!.predicted_stars}</b>
          </PredictedContainer>
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
const TopContainer = styled.header`
  & > h1 {
    margin-bottom: 12px
  }
  & > p {
    margin-top: 0px;
  }
`
const PredictedContainer = styled.div`
  align-items: baseline;
  display: flex;
  & > h2 {
    margin-right: 28px;
  }
`
const AttributesList = styled.ul`
  display: flex;
`
const AttributesListItem: StyledComponentClass<{color: string}, ITheme> = styled<{ color: string }, 'li'>('li')`
  align-items: center;
  background-color: ${({ theme, color }) => theme.color[color]};
  border: 1px solid black;
  border-radius: 6px;
  display: flex;
  margin: 0 10px 10px 0;
  padding: 5px 10px 5px 10px;
  & > span {
    margin-left: 5px;
  }
`
const ChartContainer = styled.div`
  margin: 20px 0 0 0;
`
