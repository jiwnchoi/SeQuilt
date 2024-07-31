from typing import Any, Iterable

from .RectModel import RectModel


class Event:
  def __init__(self, value: Any, position: int, occurences: Iterable) -> None:
    self.position = position
    self.occurences = set(occurences)
    self.value = value

  def __hash__(self) -> int:
    return (self.position, self.value).__hash__()

  def __eq__(self, other: "Event") -> bool:
    return self.position == other.position and self.value == other.value

  def __repr__(self) -> str:
    return (
      f"Event(Position={self.position}, Value={self.value}, # Occurences={len(self.occurences)})"
    )

  def __str__(self) -> str:
    return self.__repr__()

  def __len__(self) -> int:
    return len(self.occurences)

  def __lt__(self, other: "Event") -> bool:
    return self.position < other.position

  def diff(self, e: "Event") -> int:
    return len(self.occurences.intersection(e.occurences))

  @property
  def rect(self) -> RectModel:
    return RectModel(
      value=self.value,
      x=self.position,
      y=0,
      width=1,
      height=len(self.occurences),
    )
