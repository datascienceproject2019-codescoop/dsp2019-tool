import * as React from 'react'
import { Route, RouteProps } from 'react-router'
import styled from '../theme/styled'

import { NavBar } from './NavBar'

interface IWrappedRoute extends RouteProps {
  component: React.ComponentClass
}

const renderNoMainContainerWrapper = (Component: React.ComponentClass) => (props: RouteProps) =>
  <MainWrapper>
    <NavBar {...props}/>
    <Component {...props}/>
  </MainWrapper>

const renderWrapper = (Component: React.ComponentClass) => (props: RouteProps) =>
  <MainWrapper>
    <NavBar {...props}/>
    <MainContainer>
      <Component {...props}/>
    </MainContainer>
  </MainWrapper>

export const NoMainContainerRoute = ({ component, ...rest } : IWrappedRoute) =>
  <Route {...rest} render={renderNoMainContainerWrapper(component)}/>

export const WrappedRoute = ({ component, ...rest } : IWrappedRoute) =>
  <Route {...rest} render={renderWrapper(component)}/>

const MainWrapper = styled.div`
  font-family: 'Raleway', sans-serif;
`
const MainContainer = styled.main`
  margin: 40px auto 20px auto;
  max-width: 680px;
  @media only screen and (max-width: 720px) {
    margin: 40px 20px 20px 20px;
  }
`
