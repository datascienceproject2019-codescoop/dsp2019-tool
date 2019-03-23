import * as React from 'react'
import { NavLink } from 'react-router-dom'
import { inject } from 'mobx-react'
import { css } from 'styled-components'
import styled from '../theme/styled'

import { Stores } from '../stores'
import { AuthStore } from '../stores/AuthStore'

interface IProps {
  className?: string
  authStore?: AuthStore,
}

@inject((stores: Stores) => ({
  authStore: stores.authStore,
}))
export class NavBar extends React.PureComponent<IProps> {
  handleLogout = (e : React.MouseEvent<HTMLElement>) : void => {
    this.props.authStore!.logout()
  }
  render() {
    return (
      <NavContainer className={this.props.className}>
        <NavLinkList>
          <NavListItem><NavListLink to="/">Front page</NavListLink></NavListItem>
        </NavLinkList>
      </NavContainer>
    )
  }
}

const NavContainer = styled.nav`
  align-items: center;
  background-color: #ebf6ff;
  display: flex;
  height: 60px;
  justify-content: space-between;
`
const NavLinkList = styled.ul`
  display: flex;
  margin: 10px;
`
const NavListItem = styled.li`
  margin-right: 10px;
  &:last-child {
    margin-right: 0;
  }
`
const linkStyles = css`
  box-sizing: border-box;
  color: ${({ theme }) => theme.color.textDark };
  cursor: pointer;
  font-size: ${({ theme }) => theme.fontSize.small };
  height: 100%;
  padding: 10px 10px 10px 10px;
  text-decoration: underline;
  &:hover {
    color: ${({ theme }) => theme.color.primary};
    font-weight: 600;
  }
`
const NavListLink = styled(NavLink)`
  ${linkStyles}
`
