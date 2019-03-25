import * as React from 'react'
import { inject, observer } from 'mobx-react'
import styled from '../theme/styled'
import { MdSearch } from 'react-icons/md'
import { Link } from 'react-router-dom'

// import { Button } from '../elements/Button'
import { Input } from '../elements/Input'

import { Stores } from '../stores'
import { ProjectStore } from '../stores/ProjectStore'

interface IProps {
  projecStore?: ProjectStore
}
interface IState {
  searchText: string
}

@inject((stores: Stores) => ({
  projecStore: stores.projectStore,
}))
@observer
export class FrontPage extends React.Component<IProps, IState> {
  state = {
    searchText: ''
  }
  componentDidMount() {
    this.props.projecStore!.getProjects()
  }
  render() {
    const { projects } = this.props.projecStore!
    return (
      <Container>
        <header>
          <h1>Data science project 2019: Codescoop</h1>
          <p>
            <i>A simple app, to model crap.</i>
          </p>
        </header>
        <SearchBox>
          <label>Search</label>
          <Input placeHolder="Github project name" icon={<MdSearch size={24}/>} iconPadding="38px" fullWidth
              value={this.state.searchText || ''}
              onChange={val => this.setState({ searchText: val })}/>
        </SearchBox>
        <h2>Featured projects</h2>
        <FeaturedList >
          { projects.map((p, i) =>
          <li key={i}><Link to={p['Name with Owner']}>{p['Name with Owner']}</Link></li>
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
  & > li {
    margin: 5px;
  }
`
