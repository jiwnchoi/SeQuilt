import multiprocessing as mp
from collections import defaultdict
from functools import partial

import numpy as np


def find_chunks_subset(data_subset, threshold, max_chunk_length):
  n_sequences, n_length = data_subset.shape
  chunks = defaultdict(lambda: Chunk(None, None, None, []))
  start_map = dict()
  end_map = dict()
  start_sequence_map = dict()
  end_sequence_map = dict()

  for chunk_length in range(max_chunk_length, 0, -1):
    chunk_view = np.lib.stride_tricks.sliding_window_view(
      data_subset, (1, chunk_length)
    ).reshape(n_sequences, n_length - chunk_length + 1, chunk_length)

    chunk_hashes = np.apply_along_axis(lambda x: hash(tuple(x)), 2, chunk_view)

    unique_chunks, indices, counts = np.unique(
      chunk_hashes, return_inverse=True, return_counts=True, axis=None
    )

    mask = counts >= threshold
    for chunk_hash in unique_chunks[mask]:
      seq_indices = np.where(chunk_hashes == chunk_hash)[0]
      start = np.where(chunk_hashes == chunk_hash)[1][0]
      end = start + chunk_length
      chunk_seq = chunk_view[seq_indices[0], start]

      chunk = chunks[chunk_hash]
      if chunk.subsequence is None:
        chunk.subsequence = chunk_seq
        chunk.start = start
        chunk.end = end
      chunk.seq_indices.extend(seq_indices)
      start_map[chunk.start] = chunk
      end_map[chunk.end] = chunk
      for i in range(2, chunk_length + 1):
        start_sequence_map[(chunk.start, tuple(chunk.subsequence)[:i])] = chunk
        end_sequence_map[(chunk.end, tuple(chunk.subsequence[::-1][:i]))] = (
          chunk
        )

  return {
    "chunks": chunks,
    "start_map": start_map,
    "end_map": end_map,
    "start_sequence_map": start_sequence_map,
    "end_sequence_map": end_sequence_map,
  }


def merge_results(results):
  merged_chunks = defaultdict(lambda: Chunk(None, None, None, []))
  merged_start_map = {}
  merged_end_map = {}
  merged_start_sequence_map = {}
  merged_end_sequence_map = {}

  for result in results:
    for chunk_hash, chunk in result["chunks"].items():
      if merged_chunks[chunk_hash].subsequence is None:
        merged_chunks[chunk_hash] = chunk
      else:
        merged_chunks[chunk_hash].seq_indices.extend(chunk.seq_indices)

    merged_start_map.update(result["start_map"])
    merged_end_map.update(result["end_map"])
    merged_start_sequence_map.update(result["start_sequence_map"])
    merged_end_sequence_map.update(result["end_sequence_map"])

  return {
    "chunks": merged_chunks,
    "start_map": merged_start_map,
    "end_map": merged_end_map,
    "start_sequence_map": merged_start_sequence_map,
    "end_sequence_map": merged_end_sequence_map,
  }


def find_chunks_multiprocessing(
  data: np.ndarray,
  threshold: int = 10,
  max_chunk_length: int = 6,
  n_processes: int = None,
):
  if n_processes is None:
    n_processes = mp.cpu_count()

  chunk_size = len(data) // n_processes
  data_chunks = [
    data[i : i + chunk_size] for i in range(0, len(data), chunk_size)
  ]

  with mp.Pool(n_processes) as pool:
    results = pool.map(
      partial(
        find_chunks_subset,
        threshold=threshold,
        max_chunk_length=max_chunk_length,
      ),
      data_chunks,
    )

  return merge_results(results)


# The Chunk class definition remains the same
class Chunk:
  def __init__(self, subsequence, start, end, seq_indices):
    self.subsequence = subsequence
    self.start = start
    self.end = end
    self.seq_indices = seq_indices

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

  def add_index(self, index: int):
    self.seq_indices.append(index)

  def __repr__(self) -> str:
    return f"Chunk({self.subsequence}, {self.start}, {self.end}, #{len(self.seq_indices)})"


# Example usage
threshold = 10
max_chunk_length = 6
data = np.random.randint(0, 4, (100_000, 32))
chunks = find_chunks_multiprocessing(data, threshold, max_chunk_length)
