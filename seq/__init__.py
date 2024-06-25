from __future__ import annotations

import importlib.metadata
import os
import pathlib

import anywidget
import numpy as np
import traitlets

from .model import LabelModel, RectModel
from .utils import filter_sequences, mask_non_featured_ids

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
  # _css = (
  #   pathlib.Path(__file__).parent / "static" / "widget.css" if not dev else None
  # )
  rects = traitlets.List([]).tag(sync=True)
  labels = traitlets.List([]).tag(sync=True)
  n_sequences = traitlets.Int(0).tag(sync=True)
  n_length = traitlets.Int(0).tag(sync=True)

  width = traitlets.Int(800).tag(sync=True)
  height = traitlets.Int(600).tag(sync=True)

  grid = traitlets.Bool(False).tag(sync=True)
  sequences: np.ndarray

  def __init__(
    self,
    sequences: list[list[int]] | np.ndarray,
    labels: list[LabelModel] | list[int],
    width: int = 800,
    height: int = 600,
    grid: bool = False,
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    self.labels = (
      labels
      if isinstance(labels[0], dict)
      else [{"id": i, "label": str(i)} for i in labels]
    )
    self.featured_ids = [label["id"] for label in self.labels]
    self.update_sequences(sequences)

    self.width = width
    self.height = height
    self.grid = grid

  def update_sequences(self, sequences: list[list[int]] | np.ndarray) -> None:
    _sequences = (
      sequences if isinstance(sequences, np.ndarray) else np.array(sequences)
    )

    _sequences = mask_non_featured_ids(_sequences, self.featured_ids)
    _sequences = filter_sequences(_sequences, filter_length=1)
    print("Sequences: ", _sequences.shape)

    self.n_sequences, self.n_length = _sequences.shape
    self.sequences = sequences
    self.rects = self.get_rects(_sequences)
    print("Rects: ", len(self.rects))

  def get_rects(self, matrix: np.ndarray) -> list[RectModel]:
    result: list[RectModel] = []

    for x, col in enumerate(matrix.T):
      start = None
      for y, val in enumerate(col):
        if val != 0:
          if start is None:
            start = y
        elif start is not None:
          result.append(
            {
              "id": int(matrix[start, x]),
              "x": int(x),
              "y_start": int(start),
              "y_end": int(y - 1),
            }
          )
          start = None
      if start is not None:
        result.append(
          {
            "id": int(matrix[start, x]),
            "x": int(x),
            "y_start": int(start),
            "y_end": int(len(col) - 1),
          }
        )
    return result
