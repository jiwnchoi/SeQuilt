from __future__ import annotations

from collections import defaultdict
from typing import Hashable, Literal

import numpy as np
from tqdm import tqdm

from .Chunk import Chunk


class ChunkDatabase:
  data: np.ndarray
  n_sequences: int
  seq_length: int
  threshold: float
  max_chunk_length: int
  min_n_chunks: int

  _chunks: dict[Hashable, Chunk]
  start_map: dict[int, list[Chunk]]
  end_map: dict[int, list[Chunk]]
  continue_map: dict[tuple[str, str], list[Chunk]]
  seq_map: dict[tuple, list[Chunk]]

  def __init__(
    self,
    data: np.ndarray,
    threshold: int = 0.05,
    max_chunk_length: int | Literal["auto"] = 5,
  ) -> None:
    self.n_sequences, self.seq_length = data.shape
    self.threshold = threshold
    self.max_chunk_length = (
      max_chunk_length if max_chunk_length != "auto" else self.seq_length
    )
    self.min_n_chunks = int(self.n_sequences * self.threshold)
    self.data = data

    self._chunks = defaultdict(Chunk)
    self.start_map = defaultdict(list)
    self.end_map = defaultdict(list)
    self.start_end_map = defaultdict(list)
    self.continue_map = defaultdict(list)
    self.seq_map = defaultdict(list)
    self.length_map = defaultdict(list)

    self.find_chunks()

  def __getitem__(self, key: Hashable) -> Chunk | None:
    return self._chunks.get(key, None)

  @property
  def chunks(self):
    return sorted(
      list(self._chunks.values()),
      key=lambda x: (len(x.subsequence) * self.n_sequences * self.seq_length)
      + len(x.seq_indices),
      reverse=True,
    )

  def find_chunks(self):
    data = self.data.copy()

    for chunk_length in tqdm(range(self.max_chunk_length, 0, -1)):
      chunk_view = np.lib.stride_tricks.sliding_window_view(
        data, (1, chunk_length)
      ).reshape(
        self.n_sequences, self.seq_length - chunk_length + 1, chunk_length
      )

      for i in range(chunk_view.shape[1]):
        chunk_dict = defaultdict(list)
        for seq_idx, chunk in enumerate(chunk_view[:, i]):
          chunk_dict[tuple(chunk)].append(seq_idx)

        for chunk, seq_indices in chunk_dict.items():
          chunk = np.array(chunk)
          count = len(seq_indices)

          if np.any(chunk == 0) or (
            chunk_length > 1 and count < self.min_n_chunks
          ):
            continue

          seq_indices = np.array(seq_indices)
          data[seq_indices, i : i + chunk_length] = 0

          self.add(
            Chunk(
              start=i,
              end=i + chunk_length,
              subsequence=chunk,
              seq_indices=set(seq_indices),
            )
          )

  def add(self, chunk: Chunk):
    if chunk in self._chunks:
      self._chunks[chunk].seq_indices.update(chunk.seq_indices)
    else:
      self._chunks[chunk] = chunk
      self.start_map[chunk.start].append(chunk)
      self.end_map[chunk.end].append(chunk)
      self.start_end_map[(chunk.start, chunk.end)].append(chunk)
      self.seq_map[tuple(chunk.subsequence)].append(chunk)
      self.length_map[len(chunk.subsequence)].append(chunk)
      for i in range(len(chunk.subsequence)):
        if i > 1:
          self.continue_map[
            (f"{chunk.start}*", tuple(chunk.subsequence[:i]))
          ].append(chunk)
        if i < len(chunk.subsequence) - 2:
          self.continue_map[
            (f"*{chunk.end}", tuple(chunk.subsequence[i + 1 :]))
          ].append(chunk)

  def get_candidate(self, chunk: Chunk) -> list[Chunk]:
    candidates = {
      *self.get(start=chunk.start, sub_sequences=chunk.subsequence),
      *self.get(end=chunk.end, sub_sequences=chunk.subsequence),
    }
    for i in range(1, len(chunk.subsequence) - 1):
      left = self.get(
        start=chunk.start + i,
        end=chunk.end,
        sub_sequences=chunk.subsequence[i:],
      )
      left_continue = self.get(
        start=chunk.start + i, sub_sequences=chunk.subsequence[i:]
      )
      right = self.get(
        start=chunk.start,
        end=chunk.end - i,
        sub_sequences=chunk.subsequence[:-i],
      )
      right_continue = self.get(
        end=chunk.end - i, sub_sequences=chunk.subsequence[:-i]
      )
      candidates.update(set(left + left_continue + right + right_continue))

      if len(candidates) > 1:
        break

    return sorted(
      list(candidates),
      key=lambda x: len(x.subsequence) * self.n_sequences * self.seq_length
      + len(x.seq_indices),
      reverse=True,
    )

  def get(
    self, start: int = -1, end: int = -1, sub_sequences=None
  ) -> list[Chunk]:
    if sub_sequences is None:
      if start == -1 and end == -1:
        raise ValueError("Either start, end or sub_sequences must be provided")
      elif start == -1:
        return self.end_map[end]
      elif end == -1:
        return self.start_map[start]
      else:
        return self.start_end_map[(start, end)]

    else:
      if start == -1 and end == -1:
        return self.seq_map[tuple(sub_sequences)]
      elif start == -1:
        return self.continue_map[(f"*{end}", tuple(sub_sequences))]
      elif end == -1:
        return self.continue_map[(f"{start}*", tuple(sub_sequences))]
      else:
        c = self._chunks.get(
          Chunk(
            start=start, end=end, subsequence=sub_sequences, seq_indices=[]
          ),
          None,
        )
        return [c] if c else []

  def get_random(self):
    return np.random.choice(list(self._chunks.values()))

  def __repr__(self) -> str:
    repr = [
      "ChunkDatabase Information",
      f"Data Shape: {self.data.shape}",
      f"Threshold: {self.threshold}",
      f"Max Chunk Length: {self.max_chunk_length}",
      f"Number of Chunks: {len(self._chunks)}",
      "Number of Chunks by Length",
      *[f"{k}: {len(v)}" for k, v in self.length_map.items()],
    ]
    return "\n".join(repr)


__all__ = ["ChunkDatabase"]
