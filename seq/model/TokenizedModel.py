from typing import TypedDict

import numpy as np

TokenizedModel = TypedDict(
  "Tokenized",
  {"ids": np.ndarray, "tokens": np.ndarray},
)

__all__ = ["TokenizedModel"]
