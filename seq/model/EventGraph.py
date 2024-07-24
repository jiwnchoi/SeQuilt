from typing import TYPE_CHECKING, Iterable

import networkx as nx

if TYPE_CHECKING:
  from .Event import Event


class EventGraph(nx.Graph):
  def __init__(self):
    super().__init__()

  @property
  def events(self) -> Iterable["Event"]:
    return self.nodes

  def _add_node(self, node_for_adding: "Event", **attr):
    super().add_node(node_for_adding, **attr)
    self._make_complete(node_for_adding)

  def add_event(self, event: "Event", **attr):
    self._add_node(event, **attr)

  def add_events_from(self, events: Iterable["Event"], **attr):
    for event in events:
      self.add_event(event, **attr)

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
