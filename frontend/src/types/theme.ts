export interface IThemeColor {
  textLight: string
  textDark: string
  bg: string
  white: string
  primary: string
  secondary: string
  yellow: string
  purple: string
  lightgrey: string
  green: string
  orange: string
}

export interface ISize {
  borderWidth?: string
  fontSize?: string
  height?: string
  margin?: string
  padding?: string
  width?: string
}

export type ThemeSizeTypes = 'small' | 'medium' | 'large'

export interface IThemeSizes {
  small: ISize
  medium: ISize
  large: ISize
}

export interface ITheme {
  color: IThemeColor
  button: {
    sizes: IThemeSizes
  }
  spinner: {
    sizes: IThemeSizes
  }
  fontSize: {
    small: string
    large: string
    medium: string
    xlarge: string
    largeIcon: string
  }
}
