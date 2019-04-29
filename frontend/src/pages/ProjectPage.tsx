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

// import {
//   ScatterChart,
// } from '../components/Charts'
import { KNNTable } from '../components/KNNTable'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
import { IProjectPredicted } from '../types/project'
import { StyledComponentClass } from 'styled-components'
import { ITheme } from '../types/theme'

interface IProps extends RouteComponentProps<{ownerName: string, projectName: string}> {
  projecStore?: ProjectStore,
}
interface IState {
  loading: boolean
  error?: string
  fetchedProject?: IProjectPredicted
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
    const name = `${ownerName}/${projectName}`
    if (loading || error) {
      return (
        <Container>
          <LoadingOrErrorMsg>
            <p>{ loading ? 'loading' : error }</p>
          </LoadingOrErrorMsg>
        </Container>
      )
    }
    return (
      <Container>
        <Wrapper>
          <TopContainer>
            <h1><a href={`https://github.com/${name}`} target="__blank">{name}</a></h1>
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
            <PredictedHeader>
              <h2>Project rating: </h2>
              <b>{p!.rating}</b>
            </PredictedHeader>
            <p>
              Project rating is a simple statistic to describe a Github project's overall popularity.
              Calculated from a Github project's available information such as
              stars, forks, contributors, last updated timestamp and are issues or wiki enabled. Using the Libraries.io's
              SourceRank algorithm as its basis, it was created to be a more robust version of it without some of its
              more obscure features. Also we try to normalize the values between 0 and 5, where the mean value of our
              500 000 test set lies somewhere around 1.8. Very few projects get a value higher than 4, and only 2 gained
              5 in that 500 000. For a hugely successful project the rating might go over 5 since it's not bound.
            </p>
          </PredictedContainer>
          <PredictedContainer>
            <PredictedHeader>
              <h2>Predicted stars: </h2>
              <b>{p!.predicted_stars}</b>
            </PredictedHeader>
            <p>
              This is the predicted value of a project's star count using a simple linear regression. The features picked
              for the regression are computed using a lasso which gives approximately 20 features of the Libraries.io dataset.
              It's most accurate with more popular projects with higher star count than lower star count projects.
            </p>
          </PredictedContainer>
          <ChartContainer>
            <h2>Similar projects</h2>
            <KNNTable names={p!.knn_names} distances={p!.knn_distances}/>
          </ChartContainer>
        </Wrapper>
        <PlotContainer>
          <h2>Rating timeline</h2>
          <img src={`${process.env.REACT_APP_API_URL}/images/timeseries/rating?repo=${name}`}></img>
          {/**
            /api/images/timeseries/stars
            /api/images/timeseries/forks
            /api/images/timeseries/closedissues
            /api/images/timeseries/commits
            /api/images/timeseries/contributors
            /api/images/timeseries/issues
            /api/images/timeseries/watchers
           */}
        </PlotContainer>
      </Container>
    )
  }
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
`
const LoadingOrErrorMsg = styled.div`
  margin-top: 100px;
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
  display: flex;
  flex-direction: column;
  & > p {
    margin: 0;
  }
`
const PredictedHeader = styled.div`
  align-items: center;
  display: flex;
  justify-content: flex-start;
  & > h2 {
    margin: 10px 28px 10px 0;
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
  margin: 0 0 0 0;
`
const PlotContainer = styled.div`
  display: flex;
  flex-direction:column;
  align-items: center;
  & > img {
    width: 100%;
    height: auto;
  }
`
