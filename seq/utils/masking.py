from __future__ import annotations

import numpy as np


def mask_small_clusters(
  sequences: np.ndarray, min_cluster_size: int = 2
) -> np.ndarray:
  sequences = sequences.copy()
  n = len(sequences)
  m = len(sequences[0])
  for j in range(m):
    diff = np.diff(sequences[:, j])
    splits = np.where(diff != 0)[0] + 1
    splits = [0, *splits, n]
    for i in range(0, len(splits) - 1):
      if splits[i + 1] - splits[i] < min_cluster_size:
        sequences[splits[i] : splits[i + 1], j] = 0
  return sequences


def mask_non_featured_ids(
  sequences: list[list[int]] | np.ndarray, label_ids: list[int]
) -> np.ndarray:
  if not isinstance(sequences, np.ndarray):
    sequences = np.array(sequences)

  mask = np.isin(sequences, label_ids)
  sequences = sequences * mask

  return sequences


__all__ = [
  "mask_small_clusters",
  "mask_non_featured_ids",
]
