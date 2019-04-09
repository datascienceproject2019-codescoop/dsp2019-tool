import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { MdSearch } from 'react-icons/md'
import { Link } from 'react-router-dom'

// import { Button } from '../elements/Button'
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
        <header>
          <h1><a href="https://github.com/datascienceproject2019-codescoop/dsp2019-tool" target="__blank">
            Data science project 2019: Codescoop
          </a></h1>
          <p>
            <i>Is a library good or not, we'll show you!</i>
          </p>
        </header>
        <SearchBox>
          <label>Search</label>
          <Input placeHolder="Github project name" icon={<MdSearch size={24}/>} iconPadding="38px" fullWidth
              value={this.state.searchText || ''}
              onChange={this.handleSearch}/>
        </SearchBox>
        <h2>Featured projects</h2>
        <FeaturedList >
          { projects.map((p, i) =>
          <li key={i} className={shownResults[i] ? '' : 'hidden'}>
            <Link to={`projects/${p['Name with Owner']}`}>{p['Name with Owner']}</Link>
          </li>
          )}
        </FeaturedList >
      </Container>
    )
  }
}

const Container = styled.div`
`
const SearchBox = styled.div`
  flex-direction: column;
  display: flex;
  width: 300px;
`
const FeaturedList = styled.ul`
  .hidden {
    visibility: hidden;
    display: none;
  }
  & > li {
    margin: 5px;
  }
`
