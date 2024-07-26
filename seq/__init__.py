from __future__ import annotations

import importlib.metadata
import os
import pathlib

import anywidget
import traitlets

from .model import LabelModel, RectModel, WidgetModel

dev = os.environ.get("ANYWIDGET_DEV") == "1"

try:
  __version__ = importlib.metadata.version("seq")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"


class Widget(anywidget.AnyWidget, WidgetModel):
  _esm = (
    pathlib.Path(__file__).parent / "static" / "widget.js"
    if not dev
    else "http://localhost:5173/widget/widget.ts?anywidget"
  )

  labels = traitlets.List([]).tag(sync=True)
  sequlets = traitlets.List([]).tag(sync=True)

  width = traitlets.Int(800).tag(sync=True)
  height = traitlets.Int(600).tag(sync=True)

  grid = traitlets.Bool(False).tag(sync=True)

  def __init__(
    self,
    sequlets: list[list[RectModel]] = [],
    labels: list[LabelModel] = [],
    width: int = 800,
    height: int = 600,
    grid: bool = False,
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    self.sequlets = sequlets
    self.labels = labels
    self.width = width
    self.height = height
    self.grid = grid
