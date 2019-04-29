import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { MdSearch } from 'react-icons/md'
import { GoMarkGithub } from 'react-icons/go'

import { FeaturedProjectsTable } from '../components/FeaturedProjectsTable'
import { Button } from '../elements/Button'
import { Input } from '../elements/Input'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'
import { IProject } from 'src/types/project'

interface IProps {
  projecStore?: ProjectStore
}
interface IState {
  loading: boolean
  error: string
  searchText: string
  githubInput: string
  shownResults: boolean[]
}

@inject((stores: Stores) => ({
  projecStore: stores.projectStore,
}))
@observer
export class FrontPage extends React.Component<IProps, IState> {
  state = {
    loading: true,
    error: '',
    searchText: '',
    githubInput: '',
    shownResults: []
  }
  async componentDidMount() {
    const result = await this.props.projecStore!.getProjects()
    if (result) {
      this.setState({
        loading: false,
        shownResults: Array(result.length).fill(true)
      })
    } else {
      this.setState({
        loading: false,
        error: 'Getting the projects from the API failed. Whops.'
      })
    }
  }
  projectIncludesString(p: IProject, s: string) {
    const name = p['Name with Owner'].toLowerCase()
    const str = s.toLowerCase()
    return name.includes(str)
  }
  handleSearch = (input: string) => {
    this.setState({
      searchText: input,
      shownResults: this.props.projecStore!.projects.map(p => this.projectIncludesString(p, input))
    })
  }
  render() {
    const { projects } = this.props.projecStore!
    const { shownResults } = this.state
    return (
      <Container>
        <Header>
          <h1>Project Scooper</h1>
          <h3>
            The app for Data science project 2019, group Codescoop.
            <a href="https://github.com/datascienceproject2019-codescoop/dsp2019-tool" target="__blank"> Source</a>
          </h3>
          <p>
            <i>Is a library good or not, we'll show you!</i>
          </p>
        </Header>
        <Divider />
        <Description>
          <h2>Description</h2>
          <p>
            This application predicts and computes three types of models for Github projects using
            the <a href="https://libraries.io">https://libraries.io</a> datasets for training. These are: <strong>linear regression</strong>
            , <strong>KNN</strong> and our custom <strong>project-rating</strong>, a variation of the SourceRank algorithm calculated
            by the Libraries.io.
          </p>
          <p>
            For KNN we have only calculated the nearest neighbours for a subset of the data, 500 000 to be precise. Therefore, it's
            capabilities are limited. For the linear regression and project rating however, we offer a integration with Github API
            where you can input any Github project and we'll compute the regression and rating using the fetched values.
            Computation for that data is though a little bit slower. And if nothing comes out and the featured projects list on this page
            is empty, it means that our backend server hosted on cs.users.helsinki is down, ups. You can always run the model locally,
            with some effort but it should be doable.
          </p>
          <p>
            The source code for this project lies here <a href="https://github.com/datascienceproject2019-codescoop">
            https://github.com/datascienceproject2019-codescoop</a>. All code is open-source and available in accordance to
            Libraries.io's terms of use.
          </p>
        </Description>
        <Divider />
        <DatasetsContainer>
          <Dataset>
            <h3>Github data (no KNN, slower but up-to-date)</h3>
            <SearchBox>
              <label>Owner and repository name</label>
              <Input placeholder="Eg. facebook/react" icon={<GoMarkGithub size={24}/>} iconPadding="38px" fullWidth
                  value={this.state.githubInput || ''}
                  onChange={val => this.setState({ githubInput: val })}/>
            </SearchBox>
            <GithubButton>Find</GithubButton>
          </Dataset>
          <Dataset>
            <h3>Libraries.io data of 2018-03-12 (500 000 projects) <a href="https://libraries.io/data">source</a></h3>
            <SearchBox>
              <label>Search</label>
              <Input placeholder="Project name" icon={<MdSearch size={24}/>} iconPadding="38px" fullWidth
                  value={this.state.searchText || ''}
                  onChange={this.handleSearch}/>
            </SearchBox>
            <h2>Featured projects</h2>
            <FeaturedProjectsTable projects={projects} shownProjects={shownResults}/>
          </Dataset>
        </DatasetsContainer>
      </Container>
    )
  }
}

const Container = styled.div`
`
const Header = styled.header`
  margin: 0;
  & > h1 {
    margin: 0 0 0.25em 0;
    text-decoration: underline;
  }
  & > h3 {
    margin: 0 0 0.25em 0;
  }
  & > p {
    margin: 0;
  }
`
const Divider = styled.hr`
  margin: 1.4em 0 1.4em 0;
`
const Description = styled.article`
  display: flex;
  flex-direction: column;
  & > h2 {
    margin: 0 0 0.25em 0;
  }
  & > p {
    margin: 0.5em 0 0.5em 0;
  }
  & > p:last-child {
    margin: 0;
  }
`
const DatasetsContainer = styled.section`
  display: flex;
  flex-direction: column;
`
const Dataset = styled.div`
  &:first-child {
    margin-bottom: 1.4em;
  }
  & > h3 {
    margin: 0 0 1em 0;
  }
`
const GithubButton = styled(Button)`
  margin: 15px 0 25px 0;
  width: 150px;
`
const SearchBox = styled.div`
  flex-direction: column;
  display: flex;
  width: 300px;
`
