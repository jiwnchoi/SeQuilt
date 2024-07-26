from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
  from numpy import ndarray


class TokenizedModel(TypedDict):
  ids: ndarray
  tokens: ndarray
