from __future__ import annotations

from collections import deque

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

  @property
  def height(self):
    return sum([chunk.height for chunk in self.path])

  @property
  def start(self):
    return min([chunk.start for chunk in self.path])

  @property
  def end(self):
    return max([chunk.end for chunk in self.path])

  @property
  def width(self):
    return self.end - self.start

  @property
  def size(self):
    return sum([chunk.size for chunk in self.path])

  @property
  def shape(self):
    return self.height, self.width

  @property
  def sequlet(self):
    canvas = np.zeros(self.shape)

    current_index = 0
    for chunk in self.path:
      canvas[
        current_index : current_index + chunk.height, chunk.start : chunk.end
      ] = chunk.subsequence
      current_index += chunk.height
    return canvas

  def draw(self, canvas: np.ndarray, n_steps: int) -> np.ndarray | None:
    if canvas.shape[1] != self.width:
      raise ValueError("Width of subcanvas does not match width of cluster")

    max_start = canvas.shape[0] - self.height + 1
    sequlet = self.sequlet

    for i in range(0, max_start, n_steps):
      subcanvas = canvas[i : i + self.height]
      target = sequlet != 0
      if np.all(subcanvas[target] == 0):
        subcanvas[target] = sequlet[target]
        return canvas

    return None

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
