from __future__ import annotations

from typing import TypeVar

from .Event import Event
from .RectModel import RectModel

T = TypeVar("T")


class Sequlet:
  id: int
  events: list["Event"]

  def __init__(self, id: int, events: list["Event"]) -> None:
    self.id = id
    self.events = events

  def __repr__(self) -> str:
    return f"Sequlet(events={self.events})"

  def __get_rects(self, inverse: bool = False) -> list["RectModel"]:
    if len(self.events) == 0:
      return []

    if len(self.events) == 1:
      return [self.events[0].rect.model_copy()]

    rects = [e.rect.model_copy() for e in self.events]

    for i in range(1, len(self.events)):
      s_event_idx = i - 1 if len(self.events[i - 1]) < len(self.events[i]) else i
      b_event_idx = i if s_event_idx == i - 1 else i - 1

      s_event = self.events[s_event_idx]
      b_event = self.events[b_event_idx]

      s_rect = rects[s_event_idx]
      b_rect = rects[b_event_idx]

      len_intersect = len(s_event.occurences.intersection(b_event.occurences))

      if inverse and len_intersect == len(s_event):
        s_rect.y += len(b_event) - len(s_event)

      if inverse and len_intersect != len(s_event):
        s_rect.y += len(b_event) - len_intersect

      if not inverse and len_intersect == len(s_event):
        pass  # Remain y = 0

      if not inverse and len_intersect != len(s_event):
        b_rect.y += len(s_event) - len_intersect

    return rects

  @property
  def rect_variants(self) -> list[list["RectModel"]]:
    if len(self.events) == 0:
      return []

    if len(self.events) == 1:
      return [[self.events[0].rect.model_copy()]]

    return [self.__get_rects(), self.__get_rects(inverse=True)]
