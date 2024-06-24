from __future__ import annotations

import importlib.metadata
import os
import pathlib

import anywidget
import numpy as np
import traitlets

from .model import LabelModel
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
  _css = (
    pathlib.Path(__file__).parent / "static" / "widget.css" if not dev else None
  )
  sequences = traitlets.List([]).tag(sync=True)
  labels = traitlets.List([]).tag(sync=True)

  def __init__(
    self,
    sequences: list[list[int]] | np.ndarray,
    labels: list[LabelModel] | list[int],
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    self.labels = (
      labels
      if isinstance(labels[0], dict)
      else [{"id": i, "label": str(i)} for i in labels]
    )

    self.update_sequences(sequences)

  def update_sequences(self, sequences: list[list[int]] | np.ndarray) -> None:
    _sequences = (
      sequences if isinstance(sequences, np.ndarray) else np.array(sequences)
    )

    label_ids = [label["id"] for label in self.labels]

    _sequences = mask_non_featured_ids(_sequences, label_ids)
    _sequences = filter_sequences(_sequences, filter_length=0)

    self.sequences = _sequences.tolist()
