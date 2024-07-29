from functools import cached_property
from typing import TYPE_CHECKING

import numpy as np

from ..utils import jaccard_similarity_mod

if TYPE_CHECKING:
  from .Event import Event


class Sequlet:
  events: list["Event"]
  value_sequence: np.ndarray

  left_occurences: list[set]
  right_occurences: list[set]

  left_position: int
  right_position: int

  def __init__(self, event: "Event") -> None:
    self._check_event(event)

    self.events = [event]
    self.value_sequence = np.array([event.value])

    self.left_occurences = [self.events[0].occurences]
    self.right_occurences = [self.events[0].occurences]

    self.left_position = event.position
    self.right_position = event.position

  def __repr__(self) -> str:
    r = f"Sequlet(#Events={len(self.events)}, ValueSequence={self.value_sequence})"
    r += "\n\t".join([f"{e}" for e in self.events])
    return r

  def __str__(self) -> str:
    return self.__repr__()

  def __len__(self) -> int:
    return len(self.events)

  def __getitem__(self, index: int) -> "Event":
    return self.events[index]

  @cached_property
  def left_position(self) -> int:
    return min(e.position for e in self.events)

  @cached_property
  def right_position(self) -> int:
    return max(e.position for e in self.events)

  def _check_event(self, event) -> None:
    if not isinstance(event, Event):
      raise ValueError("Event must be of type Event.")

    if self.events and len(self.events) and event in self.events:
      raise ValueError("Event already exists")

  def append(self, event: "Event") -> None:
    self._check_event(event)

    # Check appendable
    if event.position < self.right_position:
      raise ValueError("Event position is not appendable.")

    intersects = [
      event.occurences.intersection(e.occurences) for e in self.events
    ]
    intersect_sims = [jaccard_similarity_mod(i) for i in intersects]
    print(intersects, intersect_sims)

    # max, ...

    # ..., max

    # 1, 1, not 1, ...

    # ..., not 1, 1, 1
