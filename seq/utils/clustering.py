from __future__ import annotations

import sys

import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

from .distance import get_distance_numba

sys.setrecursionlimit(10**9)


def cluster_sequences(sequences: list[list[int]] | np.ndarray) -> np.ndarray:
  sequences = np.array(sequences)
  # dist = get_distance(sequences)
  dist = get_distance_numba(sequences)
  dist = squareform(dist)
  linkage_matrix = linkage(dist, method="average")
  dendrogram_data = dendrogram(linkage_matrix, no_plot=True)
  order = dendrogram_data["leaves"]
  order = np.array(order)
  return np.array(sequences)[order]


__all__ = ["cluster_sequences"]
