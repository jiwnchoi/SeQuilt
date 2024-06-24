import numpy as np


def get_distance(x: np.ndarray) -> np.ndarray:
  seq1 = x[:, np.newaxis, :]
  seq2 = x[np.newaxis, :, :]
  distances = seq1 != seq2
  zero_distances = np.logical_and(seq1 == 0, seq2 == 0)
  distances = np.maximum(distances, zero_distances)

  distances = np.sum(distances, axis=2) / x.shape[1]
  np.fill_diagonal(distances, 0)

  return distances


__all__ = ["get_distance"]
