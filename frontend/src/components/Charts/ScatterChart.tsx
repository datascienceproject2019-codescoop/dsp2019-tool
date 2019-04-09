import * as React from 'react'
import {
  ScatterChart as SChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts'
import styled from '../../theme/styled'

interface IProps {
  names: string[]
  distances: number[]
}

class ScatterChartClass extends React.PureComponent<IProps> {
  render() {
    const { names, distances } = this.props
    const combined = names.map((n, i) => ({ name: n, distance: distances[i], y: i % 2 }))
    return (
      <SChart
        width={400}
        height={400}
        margin={{
          top: 20, right: 20, bottom: 20, left: 20,
        }}
      >
        <CartesianGrid />
        <XAxis type="number" dataKey="distance" name="distance" unit="dist" domain={[-1, 'auto']}/>
        <YAxis dataKey="y" domain={[-2, 2]}/>
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="Repository name" data={combined} fill="#8884d8">
        </Scatter>
      </SChart>
    )
  }
}
export const ScatterChart = styled(ScatterChartClass)``
