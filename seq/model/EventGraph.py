from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterable, Iterator

import networkx as nx
import numpy as np

if TYPE_CHECKING:
  from .Event import Event


class EventGraph(nx.Graph):
  def __init__(self, data: np.ndarray | list[list]):
    super().__init__()
    if not isinstance(data, (np.ndarray, list)):
      raise ValueError("Data must be a 2-dimensional array or list")

    events = self._count_events(data)

    if len(events) == 0:
      raise ValueError("No events found in the data")

    self.add_events_from(events)

  @cached_property
  def events(self) -> Iterator["Event"]:
    return self.nodes

  def add_event(self, event: "Event", **attr):
    self._add_node(event, **attr)

  def add_events_from(self, events: Iterable["Event"], **attr):
    for event in events:
      self.add_event(event, **attr)

  def _count_events(self, data: np.ndarray | list[list[Any]]) -> list["Event"]:
    if not isinstance(data, np.ndarray):
      try:
        data = np.array(data)
      except ValueError:
        raise ValueError(
          "Sequence data must be a 2-dimensional array and the values must be hashable"
        )

    if len(data.shape) != 2:
      raise ValueError("Sequence data must be 2-dimensional array")

    events = []

    for position in range(data.shape[1]):
      unique = np.unique(data[:, position])

      events.extend(
        [
          Event(
            value,
            position,
            np.argwhere(data[:, position] == value).flatten().tolist(),
          )
          for value in unique
        ]
      )

    return events

  def _add_node(self, node_for_adding: "Event", **attr):
    super().add_node(node_for_adding, **attr)
    self._make_complete(node_for_adding)

  def _make_complete(self, new_node: "Event"):
    for node in self.events:
      if node != new_node and node.position != new_node.position:
        weight = new_node.diff(node)
        super().add_edge(new_node, node, weight=weight)

  def add_edge(self, **attr):
    raise NotImplementedError(
      f"Cannot manually add edges in {self.__class__.__name__}"
    )

  def add_edges_from(self, **attr):
    raise NotImplementedError(
      f"Cannot manually add edges in {self.__class__.__name__}"
    )

  def remove_edge(self):
    raise NotImplementedError(
      f"Cannot remove edges in {self.__class__.__name__}"
    )

  def remove_edges_from(self):
    raise NotImplementedError(
      f"Cannot remove edges in {self.__class__.__name__}"
    )

  def add_node(self, node_for_adding, **attr):
    raise NotImplementedError(
      f"Cannot manually add nodes in {self.__class__.__name__}"
    )

  def add_nodes_from(self, nodes_for_adding, **attr):
    raise NotImplementedError(
      f"Cannot manually add nodes in {self.__class__.__name__}"
    )
