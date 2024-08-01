from __future__ import annotations

from functools import cached_property
from heapq import heappop, heappush
from typing import Any, Iterable, Iterator

import networkx as nx
import numpy as np

from .Event import Event


class EventGraph(nx.Graph):
  def __init__(self, data: np.ndarray | list[list]):
    super().__init__()
    if not isinstance(data, (np.ndarray, list)):
      raise ValueError("Data must be a 2-dimensional array or list")

    events = self._count_events(data)

    if len(events) == 0:
      raise ValueError("No events found in the data")

    self.edge_heap = []
    self.add_events_from(events)

  @cached_property
  def events(self):
    return self.nodes

  @property
  def sorted_edges(self) -> Iterator[tuple["Event", "Event", int | float]]:
    while self.edge_heap:
      weight, node1, node2 = heappop(self.edge_heap)
      if not self.has_node(node1) or not self.has_node(node2):
        continue
      yield node2, node1, -weight

  def add_event(self, event: "Event", **attr):
    self._add_node(event, **attr)

  def add_events_from(self, events: Iterable["Event"], **attr):
    for event in events:
      self.add_event(event, **attr)

  def remove_event(self, event: "Event"):
    super().remove_node(event)

  def remove_events_from(self, events: Iterable["Event"]):
    for event in events:
      self.remove_event(event)

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
          if value
        ]
      )

    return events

  def _add_node(self, node_for_adding: "Event", **attr):
    super().add_node(node_for_adding, **attr)
    self._make_adjacent_edges(node_for_adding)

  def _make_adjacent_edges(self, new_node: "Event"):
    for node in self.events:
      if node != new_node and abs(new_node.position - node.position) == 1:
        diff = new_node.diff(node)
        if diff == 0:
          continue
        super().add_edge(new_node, node, weight=diff)
        heappush(self.edge_heap, (-diff, new_node, node))

  # Override to disable networkx.Graph methods

  def add_edge(self, u_of_edge, v_of_edge, **attr):
    raise NotImplementedError(f"Cannot manually add edges in {self.__class__.__name__}")

  def add_edges_from(self, ebunch_to_add, **attr):
    raise NotImplementedError(f"Cannot manually add edges in {self.__class__.__name__}")

  def remove_edge(self, u, v):
    raise NotImplementedError(f"Cannot manually remove edges in {self.__class__.__name__}")

  def remove_edges_from(self, ebunch):
    raise NotImplementedError(f"Cannot manually remove edges in {self.__class__.__name__}")

  def add_node(self, node_for_adding, **attr):
    raise NotImplementedError(f"Cannot manually add nodes in {self.__class__.__name__}")

  def add_nodes_from(self, nodes_for_adding, **attr):
    raise NotImplementedError(f"Cannot manually add nodes in {self.__class__.__name__}")

  def remove_node(self, n):
    raise NotImplementedError(f"Cannot manually remove nodes in {self.__class__.__name__}")
