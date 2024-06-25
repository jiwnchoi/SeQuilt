from typing import TypedDict

RectModel = TypedDict(
  "RectModel",
  {
    "rect_id": str,
    "id": int,
    "x": int,
    "y_start": int,
    "y_end": int,
  },
)

__all__ = ["RectModel"]
