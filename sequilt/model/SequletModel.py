from .Event import Event
from .RectModel import RectModel


class SequletModel:
  events: list["Event"]

  def __init__(self, events: list["Event"]) -> None:
    self.events = events

  def __get_rect_variants(self, inverse: bool = False) -> list["RectModel"]:
    rects = [e.rect.model_copy() for e in self.events][:: (-1 if inverse else 1)]

    for i in range(1, len(rects)):
      rects[i].y += len(self.events[i].occurences.difference(self.events[i - 1].occurences))

    return rects

  @property
  def rect_variants(self) -> list[list["RectModel"]]:
    return [self.__get_rect_variants(), self.__get_rect_variants(inverse=True)]
