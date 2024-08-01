from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


class BaseTokenizer:
  def __init__(self):
    self._token_to_id = {"[MASK]": 0}
    self._id_to_token = {0: "[MASK]"}

  def encode(self, sequence: T) -> list[T]:
    raise NotImplementedError()

  def encode_batch(self, sequences: list[T]) -> list[T]:
    return [self.encode(sequence) for sequence in sequences]

  def decode(self, sequences: T) -> T:
    raise NotImplementedError()

  def decode_batch(self, sequences: list[T]) -> list[T]:
    return [self.decode(sequence) for sequence in sequences]

  def get_vocab(self) -> dict:
    return self._token_to_id

  def get_vocab_size(self) -> int:
    return len(self._token_to_id)

  def token_to_id(self, token: str) -> int | None:
    if token not in self._token_to_id:
      return None
    return self._token_to_id[token]

  def id_to_token(self, id: int) -> str | None:
    if id not in self._id_to_token:
      return None
    return self._id_to_token[id]


__all__ = ["BaseTokenizer"]
