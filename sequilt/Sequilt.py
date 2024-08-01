import json
import os
import pathlib

import anywidget
import numpy as np
from traitlets import Bool, Int, List

from .model import LabelModel, RectModel, Sequlet


class Sequilt(anywidget.AnyWidget):
  labels = List([]).tag(sync=True)
  sequlets = List([]).tag(sync=True)

  width = Int(800).tag(sync=True)
  height = Int(600).tag(sync=True)

  grid = Bool(False).tag(sync=True)

  __sequlet_rects: list[list[RectModel]]
  __canvas: np.ndarray

  __sequence_length: int
  __n_sequences: int

  def __init__(
    self,
    sequence_length: int,
    n_sequences: int,
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

    self.labels = [label.model_dump() for label in labels]
    self.width = width
    self.height = height
    self.grid = grid

    self.__sequence_length = sequence_length
    self.__n_sequences = n_sequences
    self.__canvas = np.zeros((self.__sequence_length, self.__n_sequences * 2))
    self.__sequlet_rects = []

  @property
  def density(self) -> float:
    return np.count_nonzero(self.__canvas) / self.__canvas.size

  @property
  def shape(self) -> tuple[int, int]:
    return self.canvas.shape

  @property
  def canvas(self) -> np.ndarray:
    return self.__canvas[~np.all(self.__canvas == 0, axis=(0, 1))]

  def __len__(self) -> int:
    return len(self.sequlets)

  def __is_canvas_drawable(self, rects: list["RectModel"], offset: int) -> bool:
    if max(offset + rect.height + rect.y for rect in rects) > self.__canvas.shape[1]:
      self.__canvas = np.pad(self.__canvas, ((0, 0), (0, 10000)), mode="constant")

    return all(
      np.all(
        self.__canvas[
          rect.x : rect.x + rect.width,
          offset + rect.y : offset + rect.y + rect.height,
        ]
        == 0
      )
      for rect in rects
    )

  def __get_drawble_offset(self, rects: list["RectModel"]) -> int:
    all_rects = [rect for sequlet_rect in self.__sequlet_rects for rect in sequlet_rect]
    offsets = {
      rect.y + rect.height - target_rect.y
      for target_rect in rects
      for rect in all_rects
      if rect.x == target_rect.x
    }
    offsets.add(0)

    return next((offset for offset in offsets if self.__is_canvas_drawable(rects, offset)), 0)

  def __draw_rect(self, rect: "RectModel") -> None:
    self.__canvas[
      rect.x : rect.x + rect.width,
      rect.y : rect.y + rect.height,
    ] = rect.value

  def draw_sequlet(self, sequlet: "Sequlet") -> None:
    rect_variants = sequlet.rect_variants
    y_offsets = [self.__get_drawble_offset(rects) for rects in rect_variants]
    idx = min(range(len(y_offsets)), key=lambda i: y_offsets[i])
    y_offset = y_offsets[idx]

    for rect in rect_variants[idx]:
      rect.y += y_offset
      self.__draw_rect(rect)

    self.__sequlet_rects.append(rect_variants[idx])
    self.sequlets = [
      *self.sequlets,
      {
        "id": sequlet.id,
        "rects": [rect.model_dump() for rect in rect_variants[idx]],
      },
    ]
