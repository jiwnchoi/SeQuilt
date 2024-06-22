from __future__ import annotations

from nltk.tokenize import word_tokenize
from tokenizers import Tokenizer


class NLTKTokenizer:
  def __init__(self):
    self.token_to_id = {}
    self.id_to_token = {}

  def encode(self, text: str) -> list[str]:
    tokens = word_tokenize(text)
    for token in tokens:
      if token not in self.token_to_id:
        self.token_to_id[token] = len(self.token_to_id) + 1
        self.id_to_token[self.token_to_id[token]] = token

    return {
      "ids": [self.token_to_id[token] for token in tokens],
      "tokens": tokens,
    }

  def encode_batch(self, texts: list[str]) -> list[dict]:
    return [self.encode(text) for text in texts]

  def decode(
    self, tokens: list[str] | None = None, ids: list[int] | None = None
  ) -> str:
    if tokens is None and ids is None:
      raise ValueError("Either tokens or ids should be provided")

    if tokens is not None:
      return " ".join(tokens)

    else:
      return " ".join([self.id_to_token[id] for id in ids])

  def decode_batch(self, batch: list[dict]) -> list[str]:
    return [self.decode(**item) for item in batch]

  def get_vocab(self) -> dict:
    return self.token_to_id

  def get_vocab_size(self) -> int:
    return len(self.token_to_id)

  def token_to_id(self, token: str) -> int | None:
    if token not in self.token_to_id:
      return None
    return self.token_to_id[token]

  def id_to_token(self, id: int) -> str | None:
    if id not in self.id_to_token:
      return None
    return self.id_to_token[id]


def get_tokenizer(name: str = "nltk") -> Tokenizer | NLTKTokenizer:
  if name == "nltk":
    return NLTKTokenizer()
  else:
    _tokenizer: Tokenizer = Tokenizer.from_pretrained(name)
    return _tokenizer


__all__ = ["get_tokenizer", "NLTKTokenizer"]
