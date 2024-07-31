import numpy as np

from .RectModel import RectModel
from .SequletModel import SequletModel


class EventCanvas:
  __canvas: np.ndarray

  width: int
  density: float
  shape: tuple[int, int]
  sequlet_rects: list[list["RectModel"]]

  def __init__(self, width: int, initial_height: int = 10000) -> None:
    self.width = width
    self.__canvas = np.zeros((width, initial_height))
    self.sequlet_rects = []

  def __len__(self) -> int:
    return len(self.sequlets)

  def __repr__(self) -> str:
    repr = f"Canvas(Shape={self.shape}, #Sequlets={len(self.sequlets)}, "
    repr += f"Density={np.count_nonzero(self.__canvas) / self.__canvas.size})"
    return repr

  def __str__(self) -> str:
    return self.__repr__()

  @property
  def density(self) -> float:
    return np.count_nonzero(self.__canvas) / self.__canvas.size

  @property
  def shape(self) -> tuple[int, int]:
    return self.canvas.shape

  @property
  def canvas(self) -> np.ndarray:
    return self.__canvas[~np.all(self.__canvas == 0, axis=(0, 1))]

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

  def __get_drawble_offset(self, rects: list["RectModel"], explore_rate: float = 0.5) -> int:
    offset = 0
    step_size = round(max(rect.height for rect in rects) * explore_rate)

    while not self.__is_canvas_drawable(rects, offset):
      offset += step_size

    step_size = round(step_size * explore_rate)
    while step_size > 1:
      if offset - step_size > 0 and self.__is_canvas_drawable(rects, offset - step_size):
        offset -= step_size
      else:
        step_size = round(step_size * explore_rate)

    return offset

  def __draw_rect(self, rect: "RectModel") -> None:
    self.__canvas[
      rect.x : rect.x + rect.width,
      rect.y : rect.y + rect.height,
    ] = rect.value

  def draw_sequlet(self, sequlet: "SequletModel") -> None:
    rect_variants = sequlet.rect_variants
    y_offsets = [self.__get_drawble_offset(rects) for rects in rect_variants]

    idx = min(range(len(y_offsets)), key=lambda i: y_offsets[i])
    y_offset = y_offsets[idx]

    for rect in rect_variants[idx]:
      rect.y += y_offset
      self.__draw_rect(rect)

    self.sequlet_rects.append(rect_variants[idx])


__all__ = ["EventCanvas"]
