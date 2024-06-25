from __future__ import annotations

import numpy as np


def filter_sequences(
  sequences: list[list[int]] | np.ndarray,
  filter_length: int = 1,
) -> np.ndarray:
  if not isinstance(sequences, np.ndarray):
    sequences = np.array(sequences)
  sequences = sequences.copy()
  mask = sequences > 0

  new_sequences = sequences[np.sum(mask, axis=1) >= filter_length]
  if new_sequences.shape[0] == 0:
    raise ValueError("No remaining sequences after filtering.")

  return new_sequences


__all__ = ["filter_sequences"]
