import numpy as np
from numba import jit


@jit(nopython=True, parallel=True)
def get_distance_square(x: np.ndarray) -> np.ndarray:
  n = x.shape[0]
  m = x.shape[1]
  distances = np.zeros((n, n), dtype=np.float64)

  for i in range(n):
    for j in range(i + 1, n):
      dist = 0
      for k in range(m):
        if x[i, k] != x[j, k] or (x[i, k] == 0 and x[j, k] == 0):
          dist += 1
      distances[i, j] = distances[j, i] = dist / m

  return distances


@jit(nopython=True, parallel=True)
def get_distance_condensed(x: np.ndarray) -> np.ndarray:
  n = x.shape[0]
  m = x.shape[1]
  v_size = n * (n - 1) // 2
  v = np.zeros(v_size, dtype=np.float64)

  idx = 0
  for i in range(n):
    for j in range(i + 1, n):
      dist = 0
      for k in range(m):
        if x[i, k] != x[j, k] or (x[i, k] == 0 and x[j, k] == 0):
          dist += 1
      v[idx] = dist / m
      idx += 1

  return v


__all__ = ["get_distance_condensed", "get_distance_square"]
