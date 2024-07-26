from functools import cached_property
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
  from .Event import Event


class Sequlet:
  events: list["Event"]
  value_sequence: np.ndarray

  left_occurences: list[set]
  right_occurences: list[set]

  # Left occurences, Right occurences를 PQ
  #

  left_position: int
  right_position: int

  def __init__(self, events: list["Event"]) -> None:
    if not isinstance(events, list):
      raise ValueError("Events must be a list.")

    if len(events) != 2:
      raise ValueError("Initialize sequelet with two events.")

    if not all(isinstance(e, Event) for e in events):
      raise ValueError("All events must be of type Event.")

    self.events = events
    self.value_sequence = np.array([e.value for e in events])

    intersection_occurence = self.events[0].occurences.intersection(
      self.events[1].occurences
    )
    self.left_occurences = [
      self.events[0].occurences - intersection_occurence,
      intersection_occurence,
      self.events[1].occurences - intersection_occurence,
    ]

    self.right_occurences = self.left_occurences

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

  def _check_event(self, event: "Event") -> None:
    if not isinstance(event, Event):
      raise ValueError("Event must be of type Event.")

    if event in self.events:
      raise ValueError("Event already exists")

  def append(self, event: "Event") -> None:
    self._check_event(event)

    # Check appendable
    if event.position < self.right_position:
      raise ValueError("Event position is not appendable.")

    # Priority Queue?
