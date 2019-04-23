// import * as React from 'react'
import styled from '../theme/styled'

export const Button = styled.button`
  background-color: ${({ theme }) => theme.color.secondary };
  border: 1px solid ${({ theme }) => theme.color.textDark };
  border-radius: 4px;
  color: ${({ theme }) => theme.color.textDark };
  cursor: pointer;
  font-size: ${({ theme }) => theme.fontSize.small };
  max-width: 150px;
  padding: 0.5rem 0.5rem;
  text-decoration: none;
  &:hover {
    box-shadow: 2px 2px #039be569;
  }
  transition: 0.1s all;
`
