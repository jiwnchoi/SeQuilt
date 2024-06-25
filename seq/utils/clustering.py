from __future__ import annotations

import sys

import numpy as np
from scipy.cluster.hierarchy import leaves_list, linkage

from .distance import get_distance_condensed

sys.setrecursionlimit(10**9)


def cluster_sequences(sequences: list[list[int]] | np.ndarray) -> np.ndarray:
  sequences = np.array(sequences)
  # dist = get_distance(sequences)
  dist = get_distance_condensed(sequences)
  linkage_matrix = linkage(dist, method="average", optimal_ordering=False)
  order = leaves_list(linkage_matrix)
  return np.array(sequences)[order]


__all__ = ["cluster_sequences"]
