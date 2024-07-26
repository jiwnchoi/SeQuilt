from typing import TypedDict

import traitlets
from numpy import ndarray

class RectModel(TypedDict):
  x: int
  y: int
  width: int
  height: int

class LabelModel(TypedDict):
  value: int
  name: str

class TokenizedModel(TypedDict):
  ids: ndarray
  tokens: ndarray

class SequletModel(TypedDict):
  id: int
  rects: list[RectModel]

class WidgetModel:
  labels: traitlets.List[LabelModel]
  sequlets: traitlets.List[SequletModel]

  width: traitlets.Int
  height: traitlets.Int

  grid: traitlets.Bool

  canvasWidth: traitlets.Int
  canvasHeight: traitlets.Int

__all__ = [
  "RectModel",
  "LabelModel",
  "WidgetModel",
  "TokenizedModel",
]
