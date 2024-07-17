from __future__ import annotations

import numpy as np


class Chunk:
  def __init__(
    self,
    subsequence: np.ndarray | None = None,
    start: int = -1,
    end: int = -1,
    seq_indices: list[int] = [],
  ):
    self.subsequence = subsequence
    self.start = start
    self.end = end
    self.seq_indices: set[int] = seq_indices

  @property
  def width(self) -> int:
    return self.end - self.start

  @property
  def height(self) -> int:
    return len(self.seq_indices)

  @property
  def shape(self) -> tuple[int, int]:
    return self.height, self.width

  @property
  def size(self) -> int:
    return self.height * self.width

  def __len__(self) -> int:
    return self.height

  def __eq__(self, other):
    if not isinstance(other, Chunk):
      return False
    return (
      self.start == other.start
      and self.end == other.end
      and np.array_equal(self.subsequence, other.subsequence)
    )

  def __hash__(self):
    return hash((self.start, self.end, tuple(self.subsequence)))

  def append(self, index: int):
    self.seq_indices.add(index)

  def __repr__(self) -> str:
    return f"Chunk({self.subsequence}, {self.start}, {self.end}, #{len(self.seq_indices)})"


__all__ = ["Chunk"]
