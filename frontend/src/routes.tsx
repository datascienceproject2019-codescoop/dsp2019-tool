import * as React from 'react'
import { BrowserRouter, Redirect, Switch } from 'react-router-dom'

import { WrappedRoute } from './components/WrappedRoute'

import { FrontPage } from './pages/FrontPage'
import { StatisticsPage } from './pages/StatisticsPage'
import { ProjectPage } from './pages/ProjectPage'

export const Routes = () : React.ReactElement<any> => (
  <BrowserRouter basename={process.env.PUBLIC_URL}>
    <Switch>
      <WrappedRoute exact path="/" component={FrontPage}/>
      <WrappedRoute exact path="/statistics" component={StatisticsPage}/>
      <WrappedRoute exact path="/projects/:ownerName/:projectName" component={ProjectPage}/>
      <Redirect to="/" />
    </Switch>
  </BrowserRouter>
)
