from typing import List, TypedDict

import numpy as np
import traitlets
from pydantic import BaseModel

from .Event import Event
from .EventGraph import EventGraph
from .Sequlet import Sequlet


class RectModel(BaseModel):
  value: int
  x: int
  y: int
  width: int
  height: int


class LabelModel(BaseModel):
  value: int
  name: str


class TokenizedModel(TypedDict):
  ids: np.ndarray
  tokens: np.ndarray


class SequletRectsModel(BaseModel):
  rects: List[RectModel]


class WidgetModel:
  labels: traitlets.List[LabelModel]
  sequlets: traitlets.List[Sequlet]

  width: traitlets.Int
  height: traitlets.Int

  grid: traitlets.Bool

  canvasWidth: traitlets.Int
  canvasHeight: traitlets.Int


__all__ = [
  "RectModel",
  "LabelModel",
  "TokenizedModel",
  "SequletRectsModel",
  "WidgetModel",
  "Event",
  "EventGraph",
  "Sequlet",
]
