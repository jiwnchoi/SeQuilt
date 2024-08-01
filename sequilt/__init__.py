from __future__ import annotations

import importlib.metadata
import json
import os
import pathlib
from typing import TYPE_CHECKING

import anywidget
import traitlets

if TYPE_CHECKING:
  from .model import LabelModel, RectModel

try:
  __version__ = importlib.metadata.version("sequilt")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"


class Sequilt(anywidget.AnyWidget):
  labels = traitlets.List([]).tag(sync=True)
  sequlets = traitlets.List([]).tag(sync=True)

  width = traitlets.Int(800).tag(sync=True)
  height = traitlets.Int(600).tag(sync=True)

  grid = traitlets.Bool(False).tag(sync=True)

  def __init__(
    self,
    sequlets: list[list["RectModel"]] = [],
    labels: list["LabelModel"] = [],
    width: int = 800,
    height: int = 600,
    grid: bool = False,
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    if os.getenv("ANYWIDGET_DEV") == "1":
      vite_config = json.load(open(pathlib.Path(__file__).parent.parent / "vite.config.json"))
      self._esm = f"http://localhost:{vite_config['server']['port']}/widget/widget.ts?anywidget"
    else:
      self._esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    self.sequlets = [
      {"id": 0, "rects": [rect.model_dump() for rect in sequlet]} for sequlet in sequlets
    ]
    self.labels = [label.model_dump() for label in labels]
    self.width = width
    self.height = height
    self.grid = grid
