from __future__ import annotations

from collections import deque
from functools import cached_property

import numpy as np

from .Chunk import Chunk


class Cluster:
  path: deque

  max_start: int
  min_end: int

  def __init__(self, init_chunk: Chunk):
    self.path: deque[Chunk] = deque([init_chunk])
    self.max_start = init_chunk.start
    self.min_end = init_chunk.end

  def __len__(self):
    return len(self.path)

  def __getitem__(self, key):
    return self.path[key]

  @property
  def left(self):
    return self.path[0]

  @property
  def right(self):
    return self.path[-1]

  @cached_property
  def height(self):
    return sum([chunk.height for chunk in self.path])

  @cached_property
  def start(self):
    return min([chunk.start for chunk in self.path])

  @cached_property
  def end(self):
    return max([chunk.end for chunk in self.path])

  @cached_property
  def width(self):
    return self.end - self.start

  @cached_property
  def size(self):
    return sum([chunk.size for chunk in self.path])

  @cached_property
  def shape(self):
    return self.height, self.width

  @cached_property
  def sequlet(self):
    canvas = np.zeros(self.shape)

    current_index = 0
    for chunk in self.path:
      canvas[
        current_index : current_index + chunk.height,
        chunk.start - self.start : chunk.end - self.start,
      ] = chunk.subsequence
      current_index += chunk.height
    return canvas

  def can_draw(self, canvas: np.ndarray) -> bool:
    if canvas.shape != self.shape:
      raise ValueError(
        f"Canvas shape must match cluster shape: {canvas.shape} != {self.shape}"
      )
    sequlet = self.sequlet

    if np.all(canvas[sequlet != 0] == 0):
      return True
    return False

  def draw(self, canvas: np.ndarray) -> None:
    if canvas.shape != self.shape:
      raise ValueError("Canvas shape must match cluster shape")
    sequlet = self.sequlet

    canvas[sequlet != 0] = sequlet[sequlet != 0]

  def __repr__(self) -> str:
    return f"Cluster(shape: {self.shape}, size: {self.size})"

  def can_appendleft(self, chunk: Chunk):
    return chunk.end > self.max_start and self.left.width >= chunk.width

  def can_append(self, chunk: Chunk):
    return chunk.start < self.min_end and self.right.width >= chunk.width

  def appendleft(self, chunk: Chunk):
    self.path.appendleft(chunk)
    self.min_end = min(self.min_end, chunk.end)

  def append(self, chunk: Chunk):
    self.path.append(chunk)
    self.max_start = max(self.max_start, chunk.start)
