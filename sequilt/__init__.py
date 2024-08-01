from __future__ import annotations

import importlib.metadata

try:
  __version__ = importlib.metadata.version("sequilt")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"

from .Sequilt import Sequilt

__all__ = ["Sequilt"]
