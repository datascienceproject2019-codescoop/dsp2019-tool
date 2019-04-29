import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
import { IProjectPredicted } from '../types/project'
// import { StyledComponentClass } from 'styled-components'
// import { ITheme } from '../types/theme'

interface IProps {
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
export class StatisticsPage extends React.Component<IProps, IState> {
  state = {
    loading: false,
    error: undefined,
    fetchedProject: undefined
  }
  async componentDidMount() {
    // this.setState({ loading: true })
    // const result = await this.props.projecStore!.predictStars(`${ownerName}/${projectName}`)
    // if (result) {
    //   this.setState({
    //     loading: false,
    //     fetchedProject: result,
    //   })
    // } else {
    //   this.setState({
    //     loading: false,
    //     error: 'Unable to get the project from the API. I AM SORRY.'
    //   })
    // }
  }
  render() {
    const { loading, error } = this.state
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
        <h3>Repository-statistics Summary</h3>
        <p>
          From here you can see how the stars correlate with some of the projects' features.
        </p>
        <SnsPlot>
          <img src={`${process.env.REACT_APP_API_URL}/images/sns_image`}></img>
          <img src={`${process.env.REACT_APP_API_URL}/images/star_issue_image`}></img>
        </SnsPlot>
      </Container>
    )
  }
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`
const LoadingOrErrorMsg = styled.div`
  margin-top: 100px;
`
const SnsPlot = styled.div`
  display: flex;
  flex-direction: column;
  & > img {
    margin-bottom: 50px;
    width: 600px;
  }
`
