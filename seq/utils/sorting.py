from __future__ import annotations

import networkx as nx
import numpy as np

from .distance import get_distance_square


def sort_sequences(sequences: list[list[int]] | np.ndarray) -> np.ndarray:
  if not isinstance(sequences, np.ndarray):
    sequences = np.array(sequences)

  unique_sequences, count = np.unique(sequences, axis=0, return_counts=True)
  dist_matrix = get_distance_square(unique_sequences)

  G = nx.Graph()
  for i in range(len(dist_matrix)):
    for j in range(i + 1, len(dist_matrix)):
      G.add_edge(i, j, weight=dist_matrix[i, j])

  answer = nx.algorithms.approximation.christofides(G)
  # answer = nx.algorithms.approximation.traveling_salesman_problem(G)
  # sorted_unique_sequences = unique_sequences[np.array(answer[:-1])]

  # index_map = {i: answer[:1][i] for i in range(len(answer[:1]))}

  sorted_sequence = []

  # for i, unique_sequence in enumerate(sorted_unique_sequences):
  #   sorted_original_sequences.extend([unique_sequence] * count[index_map[i]])
  print(answer[:-1])
  for sorted_index in answer[:-1]:
    unique_sequence = unique_sequences[sorted_index]
    count_index = count[sorted_index]
    sorted_sequence.extend([unique_sequence] * count_index)

  return np.array(sorted_sequence)
