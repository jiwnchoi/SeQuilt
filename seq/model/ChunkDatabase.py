from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from typing import Hashable, Literal

import numpy as np
from tqdm import tqdm

from .Chunk import Chunk


def key(
  start: int = None,
  end: int = None,
  sequence: tuple | None = None,
):
  key = ""

  if start is not None:
    key += f"s{start}"
  if end is not None:
    key += f"e{end}"
  if sequence is not None:
    key += f"q{sequence}"

  if key == "":
    raise ValueError("No key provided")

  return key


class ChunkDatabase:
  data: np.ndarray
  n_sequences: int
  seq_length: int
  threshold: float | int
  max_chunk_length: int
  min_frequency: int

  _chunks: dict[Hashable, Chunk]
  length_map: dict[int, list[Chunk]]
  d: dict[Hashable, list[Chunk]]

  def __init__(
    self,
    data: np.ndarray,
    threshold: int | float = 100,
    max_chunk_length: int | Literal["auto"] = 5,
  ) -> None:
    self.n_sequences, self.seq_length = data.shape
    self.threshold = threshold
    self.max_chunk_length = (
      max_chunk_length if max_chunk_length != "auto" else self.seq_length
    )
    self.min_frequency = (
      self.threshold
      if isinstance(threshold, int)
      else int(self.n_sequences * threshold)
    )
    self.data = data

    self._chunks = defaultdict(Chunk)
    self.length_map = defaultdict(list)

    self.d = defaultdict(list)

    self.find_chunks()

  def __getitem__(self, key: Hashable) -> Chunk | None:
    return self._chunks.get(key, None)

  @cached_property
  def chunks(self):
    return sorted(
      list(self._chunks.values()),
      key=lambda x: (x.width, x.height),
      reverse=True,
    )

  def find_chunks(self):
    data = self.data.copy()

    for chunk_length in tqdm(range(self.max_chunk_length, 0, -1)):
      chunk_view = np.lib.stride_tricks.sliding_window_view(
        data, (1, chunk_length)
      ).squeeze(axis=2)
      org_chunk_view = chunk_view.copy()
      hashes = np.apply_along_axis(lambda x: hash(tuple(x)), 2, chunk_view)

      mask = np.any(chunk_view == 0, axis=2)

      hashes_count = np.zeros(hashes.shape)

      for col in range(hashes.shape[1]):
        _, inverse, counts = np.unique(
          hashes[:, col], return_counts=True, return_inverse=True
        )
        hashes_count[:, col] = counts[inverse]

      hashes_count[mask] = 0

      hashes_arg_sorted = np.argsort(-hashes_count, axis=1)

      min_freq = 1 if chunk_length == 1 else self.min_frequency

      for row in range(hashes.shape[0]):
        for col in hashes_arg_sorted[row]:
          if hashes_count[row, col] >= min_freq:
            if np.any(data[row, col : col + chunk_length] == 0):
              continue
            data[row, col : col + chunk_length] = 0
            self.add(
              Chunk(
                subsequence=org_chunk_view[row, col],
                start=col,
                end=col + chunk_length,
                seq_indices=set([row]),
              )
            )

    if np.any(data != 0):
      raise ValueError("Data is not fully processed")

  def add(self, chunk: Chunk):
    if chunk in self._chunks:
      self._chunks[chunk].seq_indices.update(chunk.seq_indices)
      return

    self._chunks[chunk] = chunk

    # length
    self.length_map[len(chunk.subsequence)].append(chunk)
    # start
    self.d[key(start=chunk.start)].append(chunk)
    # end
    self.d[key(end=chunk.end)].append(chunk)
    # start, end
    self.d[key(start=chunk.start, end=chunk.end)].append(chunk)
    # subsequence
    self.d[key(sequence=chunk.subsequence)].append(chunk)

    # self
    self.d[
      key(start=chunk.start, end=chunk.end, sequence=chunk.subsequence)
    ].append(chunk)

    # Continue Subsequence
    for i in range(0, chunk.width):
      self.d[key(start=chunk.start, sequence=chunk.subsequence[:-i])].append(
        chunk
      )
      self.d[key(end=chunk.end, sequence=chunk.subsequence[i:])].append(chunk)

  def get_candidate(self, chunk: Chunk) -> list[Chunk]:
    candidates: list[tuple[int, Chunk]] = []

    # Continue Subsequence Candidate
    for i in range(1, chunk.width):
      candidates.extend(
        [
          (
            chunk.width - i,
            c,
            key(start=chunk.start + i, sequence=chunk.subsequence[i:]),
          )
          for c in self.d[
            key(start=chunk.start + i, sequence=chunk.subsequence[i:])
          ]
        ]
      )
      candidates.extend(
        [
          (
            chunk.width - i,
            c,
            key(end=chunk.end - i, sequence=chunk.subsequence[:-i]),
          )
          for c in self.d[
            key(end=chunk.end - i, sequence=chunk.subsequence[:-i])
          ]
        ]
      )

    # Sliding Window Subsequence Candidate
    for window in range(1, chunk.width):
      for i in range(0, chunk.width - window):
        candidates.extend(
          [
            (
              window,
              c,
              key(
                start=chunk.start,
                end=chunk.start + window,
                sequence=chunk.subsequence[i : i + window],
              ),
            )
            for c in self.d[
              key(
                start=chunk.start,
                end=chunk.start + window,
                sequence=chunk.subsequence[i : i + window],
              )
            ]
          ]
        )
    return [
      x[1]
      for x in sorted(
        candidates,
        key=lambda x: (
          x[0],
          len(x[1].subsequence),
          len(x[1].seq_indices),
        ),
        reverse=True,
      )
    ]

  def get(self, start=None, end=None, sub_sequences=None) -> list[Chunk]:
    return self.d[key(start=start, end=end, sequence=sub_sequences)]

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
