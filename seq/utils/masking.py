from __future__ import annotations

import numpy as np


def mask_small_clusters(
  sequences: list[list[int]] | np.ndarray, min_cluster_size: int = 2
) -> np.ndarray:
  if not isinstance(sequences, np.ndarray):
    sequences = np.array(sequences)
  sequences = sequences.copy()

  masks = []
  for i in range(2 * min_cluster_size):
    left = sequences[i : -(2 * min_cluster_size - i), :]
    right = sequences[i + 1 : -(2 * min_cluster_size - i - 1) or None, :]
    masks.append(left != right)

  mask = np.logical_or.reduce(masks)
  sequences[min_cluster_size:-min_cluster_size, :][mask] = 0
  return sequences


def mask_non_featured_ids(
  sequences: list[list[int]] | np.ndarray, label_ids: list[int]
) -> np.ndarray:
  if not isinstance(sequences, np.ndarray):
    sequences = np.array(sequences)

  mask = np.isin(sequences, label_ids)
  sequences = sequences * mask

  return sequences
