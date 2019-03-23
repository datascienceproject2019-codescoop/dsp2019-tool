import * as React from 'react'
import { BrowserRouter, Redirect, Switch } from 'react-router-dom'

import { WrappedRoute } from './components/WrappedRoute'

import { FrontPage } from './pages/FrontPage'
import { ProjectPage } from './pages/ProjectPage'

export const Routes = () : React.ReactElement<any> => (
  <BrowserRouter>
    <Switch>
      <WrappedRoute exact path="/" component={FrontPage}/>
      <WrappedRoute exact path="/projects/:ownerName/:projectName" component={ProjectPage}/>
      <Redirect to="/" />
    </Switch>
  </BrowserRouter>
)
