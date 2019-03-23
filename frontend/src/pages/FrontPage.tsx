import * as React from 'react'
import { inject } from 'mobx-react'
import styled from '../theme/styled'
import { MdSearch } from 'react-icons/md'

// import { Button } from '../elements/Button'
import { Input } from '../elements/Input'

import { Stores } from '../stores'
import { AuthStore } from '../stores/AuthStore'

interface IProps {
  authStore?: AuthStore,
}
interface IState {
  searchText: string
}
@inject((stores: Stores) => ({
  authStore: stores.authStore,
}))
export class FrontPage extends React.Component<IProps, IState> {
  state = {
    searchText: ''
  }
  render() {
    return (
      <FrontPageContainer>
        <header>
          <h1>Data science project 2019: Codescoop</h1>
        </header>
        <p>
          <i>A simple app, to model crap.</i>
        </p>
        <SearchBox>
          <label>Search</label>
          <Input placeHolder="Github project name" icon={<MdSearch size={24}/>} iconPadding="38px" fullWidth
              value={this.state.searchText || ''}
              onChange={val => this.setState({ searchText: val })}/>
        </SearchBox>
        <h2>Featured projects</h2>
      </FrontPageContainer>
    )
  }
}

const FrontPageContainer = styled.div`
  margin: 40px 0 0 0;
`
const SearchBox = styled.div`
  flex-direction: column;
  display: flex;
  width: 300px;
`
