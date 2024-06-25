from __future__ import annotations

import re
from typing import Any

import numpy as np
from nltk.corpus import stopwords
from tokenizers import Encoding, Tokenizer
from tqdm import tqdm

from seq.model import TokenizedModel

from .tokenizer import NLTKTokenizer


def _encode_batch(
  text_batch: list[str],
  tokenizer: Tokenizer | NLTKTokenizer,
) -> list[TokenizedModel]:
  tokenized_batch = tokenizer.encode_batch(text_batch)
  return [
    {
      "ids": np.array(tokenized.ids),
      "tokens": np.array(tokenized.tokens, dtype=str),
    }
    if isinstance(tokenized, Encoding)
    else {
      "ids": np.array(tokenized["ids"]),
      "tokens": np.array(tokenized["tokens"], dtype=str),
    }
    for tokenized in tokenized_batch
  ]


def _encode(
  text: str,
  tokenizer: Tokenizer | NLTKTokenizer,
) -> TokenizedModel:
  tokenized = tokenizer.encode(text)
  return (
    {
      "ids": np.array(tokenized.ids, dtype=int),
      "tokens": np.array(tokenized.tokens, dtype=str),
    }
    if isinstance(tokenized, Encoding)
    else {
      "ids": np.array(tokenized["ids"], dtype=int),
      "tokens": np.array(tokenized["tokens"], dtype=str),
    }
  )


def _fix_length(
  array: np.ndarray,
  fixed_size: int = 16,
  pad_value: Any = 0,
) -> np.ndarray:
  return np.pad(
    array,
    (0, max(0, fixed_size - array.size)),
    "constant",
    constant_values=(pad_value,),
  )[:fixed_size]


def _filter_english(text: str) -> str:
  text = text.lower()
  # Remove html tags
  text = re.sub(r"<.*?>", " ", text)

  text = re.sub(r"'", " ", text)
  text = re.sub(r"[^a-zA-Z\s]", "", text)
  return text


def _filter_stopwords(text: str, stopwords: list[str]) -> str:
  return " ".join([word for word in text.split() if word not in stopwords])


def _process_text(
  text: str,
  tokenizer: Tokenizer | NLTKTokenizer,
  max_tokens: int = 16,
  stopwords: list[str] = stopwords.words("english"),
) -> TokenizedModel:
  text = _filter_english(text)
  text = _filter_stopwords(text, stopwords)
  tokenized = _encode(text, tokenizer)

  return {
    "ids": _fix_length(tokenized["ids"], max_tokens),
    "tokens": _fix_length(tokenized["tokens"], max_tokens, "[MASK]"),
  }


def get_ids(
  corpus: list[str],
  tokenizer: Tokenizer | NLTKTokenizer,
  max_tokens: int = 16,
  stopwords: list[str] = stopwords.words("english"),
) -> tuple[np.ndarray, list[np.ndarray]]:
  ids = []
  tokens = []

  for text in tqdm(corpus):
    tokenized = _process_text(text, tokenizer, max_tokens, stopwords)
    ids.append(tokenized["ids"])
    tokens.append(tokenized["tokens"])

  return np.array(ids), tokens


def tf_idf(size: tuple, ids: np.ndarray) -> np.ndarray:
  doc_term_matrix = np.zeros(size, dtype=np.float32)

  for i, id in enumerate(ids):
    doc_term_matrix[i, id] += 1

  tf = doc_term_matrix / np.sum(doc_term_matrix, axis=1)[:, np.newaxis]
  idf = np.log(len(ids) / (1 + np.sum(doc_term_matrix > 0, axis=0)))

  return tf * idf


def get_featured_ids(
  ids: list[np.ndarray],
  tokenizer: Tokenizer | NLTKTokenizer,
  n_features: int = 10,
) -> np.ndarray:
  size = (len(ids), tokenizer.get_vocab_size() + 1)
  tf_idf_matrix = tf_idf(size, np.array(ids))
  tf_idf_matrix[:, 0] = 0
  # tf_idf_matrix = tf_idf(size, np.array(ids))
  mean_tf_idf = tf_idf_matrix.mean(axis=0)

  return np.argsort(mean_tf_idf)[::-1][:n_features].tolist()


__all__ = [
  "_process_text",
  "get_ids",
  "get_featured_ids",
]
