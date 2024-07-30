import numpy as np

from . import RectModel


class Canvas:
  def __init__(self, width: int, initial_height: int = 10000) -> None:
    self.width = width
    self._canvas = np.zeros((width, initial_height))

  def get_drawble_offset(self, rect: RectModel, step: int = 100):
    offset = 0

    while True:
      if offset + rect.height > self._canvas.shape[1]:
        self._canvas = np.pad(self._canvas, ((0, 0), (0, 10000)), mode="constant")

      if np.all(self._canvas[rect.x : rect.x + rect.width, offset : offset + rect.height] == 0):
        break

      offset += step

    return offset

  def draw_rect(self, rect: RectModel) -> None:
    self._canvas[
      rect.x : rect.x + rect.width,
      rect.y : rect.y + rect.height,
    ] = rect.value

  def __repr__(self) -> str:
    repr = f"Canvas(Width={self.width}, Height={self._canvas.shape[1]}, "
    repr += f"Density={np.count_nonzero(self._canvas) / self._canvas.size})"
    return repr
