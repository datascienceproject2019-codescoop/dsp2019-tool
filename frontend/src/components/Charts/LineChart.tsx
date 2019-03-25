import * as React from 'react'
import {
  LineChart as LChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts'
import styled from '../../theme/styled'

const data = [
  {
    name: 'Date A', stars: 11700, commits: 1400, amt: 2400,
  },
  {
    name: 'Date B', stars: 13100, commits: 1698, amt: 2210,
  },
  {
    name: 'Date C', stars: 14200, commits: 2100, amt: 2290,
  },
  {
    name: 'Date D', stars: 15400, commits: 2408, amt: 2000,
  },
  {
    name: 'Date E', stars: 17000, commits: 3150, amt: 2181,
  },
  {
    name: 'Date F', stars: 18800, commits: 3800, amt: 2500,
  },
  {
    name: 'Date G', stars: 21000, commits: 4300, amt: 2100,
  },
]

interface ILineChartProps {
  className?: string
}

class LineChartClass extends React.PureComponent<ILineChartProps> {
  render() {
    const { className } = this.props
    return (
      <LChart
        className={className}
        width={500}
        height={300}
        data={data}
        margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="commits" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="stars" stroke="#82ca9d" />
      </LChart>
    )
  }
}
export const LineChart = styled(LineChartClass)``
