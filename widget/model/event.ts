export type TPointType =
  | "top-left"
  | "top-right"
  | "bottom-left"
  | "bottom-right"

export interface IRect {
  value: number
  x: number
  y: number
  width: number
  height: number
  color?: string
}

export interface IPoint {
  x: number
  y: number
  type: TPointType
}

export interface ISequlet {
  id: number
  rects: IRect[]
}

export interface ILabel {
  value: number
  name: string
}
