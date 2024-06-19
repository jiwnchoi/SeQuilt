from __future__ import annotations

import re
from typing import Any, TypedDict

import numpy as np
from nltk.corpus import stopwords
from tokenizers import Encoding, Tokenizer
from tqdm import tqdm

from seq.data.tokenizer import NLTKTokenizer

Tokenized = TypedDict(
  "Tokenized",
  {"ids": np.ndarray, "tokens": np.ndarray},
)


def _encode_batch(
  text_batch: list[str],
  tokenizer: Tokenizer | NLTKTokenizer,
) -> list[Tokenized]:
  tokenized_batch = tokenizer.encode_batch(text_batch)
  return [
    {
      "ids": np.array(tokenized.ids),
      "tokens": np.array(tokenized.tokens, dtype=str),
      "masks": np.ones(len(tokenized.ids), dtype=bool),
    }
    if isinstance(tokenized, Encoding)
    else {
      "ids": np.array(tokenized["ids"]),
      "tokens": np.array(tokenized["tokens"], dtype=str),
      "masks": np.ones(len(tokenized["ids"]), dtype=bool),
    }
    for tokenized in tokenized_batch
  ]


def _encode(
  text: str,
  tokenizer: Tokenizer | NLTKTokenizer,
) -> Tokenized:
  tokenized = tokenizer.encode(text)
  return (
    {
      "ids": np.array(tokenized.ids, dtype=int),
      "tokens": np.array(tokenized.tokens, dtype=str),
      "masks": np.ones(len(tokenized.ids), dtype=bool),
    }
    if isinstance(tokenized, Encoding)
    else {
      "ids": np.array(tokenized["ids"], dtype=int),
      "tokens": np.array(tokenized["tokens"], dtype=str),
      "masks": np.ones(len(tokenized["ids"]), dtype=bool),
    }
  )


def _fix_length(
  array: np.ndarray, fixed_size: int = 16, pad_value: Any = -1
) -> np.ndarray:
  return np.pad(
    array,
    (0, max(0, fixed_size - array.size)),
    "constant",
    constant_values=(pad_value,),
  )[:fixed_size]


def _filter_english(text: str) -> str:
  text = text.lower()
  text = re.sub(r"<.*?>", "", text)
  return re.sub(r"[^a-zA-Z\s]", "", text)


def _filter_stopwords(text: str, stopwords: list[str]) -> str:
  return " ".join([word for word in text.split() if word not in stopwords])


def process_text(
  text: str,
  tokenizer: Tokenizer | NLTKTokenizer,
  max_tokens: int = 16,
  stopwords: list[str] = stopwords.words("english"),
) -> Tokenized:
  text = _filter_english(text)
  text = _filter_stopwords(text, stopwords)
  tokenized = _encode(text, tokenizer)

  return {
    "ids": _fix_length(tokenized["ids"], max_tokens),
    "tokens": _fix_length(tokenized["tokens"], max_tokens, "<pad>"),
  }


def process_corpus(
  corpus: list[str],
  tokenizer: Tokenizer | NLTKTokenizer,
  max_tokens: int = 16,
  stopwords: list[str] = stopwords.words("english"),
) -> list[Tokenized]:
  return [
    process_text(text, tokenizer, max_tokens, stopwords)
    for text in tqdm(corpus, desc="Processing Corpus")
  ]


def get_tf_idf_matrix(ids: list[np.ndarray], n_vocab: int) -> np.ndarray:
  doc_term_matrix = np.zeros((len(ids), n_vocab), dtype=np.float32)

  for i, id in enumerate(ids):
    doc_term_matrix[i, id] += 1

  tf = doc_term_matrix / doc_term_matrix.sum(axis=1, keepdims=True)
  idf = np.log(len(ids) / (1 + (doc_term_matrix > 0).sum(axis=0)))

  return tf * idf


__all__ = ["process_text", "get_tf_idf_matrix", "process_corpus"]
