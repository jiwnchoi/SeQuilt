from __future__ import annotations

import importlib.metadata
import os
import pathlib

import anywidget
import traitlets

from .model import LabelModel

dev = os.environ.get("ANYWIDGET_DEV") == "1"

try:
  __version__ = importlib.metadata.version("seq")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"


class Widget(anywidget.AnyWidget):
  _esm = (
    pathlib.Path(__file__).parent / "static" / "widget.js"
    if not dev
    else "http://localhost:5173/widget/widget.ts?anywidget"
  )
  _css = (
    pathlib.Path(__file__).parent / "static" / "widget.css" if not dev else None
  )
  sequences = traitlets.List([]).tag(sync=True)
  labels = traitlets.List([]).tag(sync=True)

  def __init__(
    self,
    sequences: list[list[int]],
    labels: list[LabelModel] | list[int],
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    self.sequences = sequences
    self.labels = (
      labels
      if isinstance(labels[0], dict)
      else [{"id": i, "label": str(i)} for i in labels]
    )
