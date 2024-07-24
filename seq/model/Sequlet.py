from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .Event import Event


class Sequlet:
  events: set["Event"]
