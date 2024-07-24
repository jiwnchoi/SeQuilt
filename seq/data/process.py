from __future__ import annotations

import re
from typing import Any, Literal

import numpy as np
from nltk.corpus import stopwords
from tokenizers import Encoding, Tokenizer
from tqdm import tqdm

from seq.model import TokenizedModel

from .BaseTokenizer import BaseTokenizer
from .dna import DNATokenizer
from .language import NLTKTokenizer


def _encode_batch(
  text_batch: list[str],
  tokenizer: BaseTokenizer,
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
  tokenizer: BaseTokenizer,
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


def _process_dna(
  dna: str,
  tokenizer: DNATokenizer,
  max_tokens: int = 16,
) -> TokenizedModel:
  tokenized = _encode(dna, tokenizer)

  return {
    "ids": _fix_length(tokenized["ids"], max_tokens),
    "tokens": _fix_length(tokenized["tokens"], max_tokens, "[MASK]"),
  }


def _process_text(
  text: str,
  tokenizer: NLTKTokenizer,
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


def _process_dna(
  dna: str,
  tokenizer: DNATokenizer,
  max_tokens: int = 16,
) -> TokenizedModel:
  tokenized = _encode(dna, tokenizer)

  return {
    "ids": _fix_length(tokenized["ids"], max_tokens),
    "tokens": _fix_length(tokenized["tokens"], max_tokens, "[MASK]"),
  }


def get_ids(
  corpus: list[str],
  tokenizer: BaseTokenizer,
  max_tokens: int = 16,
  stopwords: list[str] = stopwords.words("english"),
) -> tuple[np.ndarray, list[np.ndarray]]:
  ids = []
  tokens = []

  for text in tqdm(corpus):
    if isinstance(tokenizer, DNATokenizer) == "dna":
      tokenized = _process_dna(text, tokenizer, max_tokens)
    if isinstance(tokenizer, NLTKTokenizer) == "language":
      tokenized = _process_text(text, tokenizer, max_tokens, stopwords)
    else:
      encoded = _encode(text, tokenizer)
      tokenized = {
        "ids": _fix_length(encoded["ids"], max_tokens),
        "tokens": _fix_length(encoded["tokens"], max_tokens, "[MASK]"),
      }
    ids.append(tokenized["ids"])
    tokens.append(tokenized["tokens"])

  return np.array(ids), tokens


def _get_doc_term_matrix(size: tuple[int, int], ids: np.ndarray) -> np.ndarray:
  doc_term_matrix = np.zeros(size, dtype=np.float32)

  for i, id in enumerate(ids):
    doc_term_matrix[i, id] += 1
  doc_term_matrix[:, 0] = 0
  return doc_term_matrix


def _tf_idf(doc_term_matrix: np.ndarray) -> np.ndarray:
  tf = doc_term_matrix / np.sum(doc_term_matrix, axis=1)[:, np.newaxis]
  idf = np.log(
    doc_term_matrix.shape[0] / (1 + np.sum(doc_term_matrix > 0, axis=0))
  )
  return tf * idf


def get_tokenizer(
  type: Literal["language", "dna"] | str, *args, **kwargs
) -> BaseTokenizer | Tokenizer:
  if type == "language":
    return NLTKTokenizer(*args, **kwargs)
  if type == "dna":
    return DNATokenizer(*args, **kwargs)
  else:
    return Tokenizer.from_pretrained(type, *args, **kwargs)


def get_featured_ids(
  ids: list[np.ndarray],
  tokenizer: BaseTokenizer,
  method: Literal["tf-idf", "count"] = "count",
  n_features: int = 10,
) -> np.ndarray:
  size = (len(ids), tokenizer.get_vocab_size() + 1)
  doc_term_matrix = _get_doc_term_matrix(size, np.array(ids))

  if method == "tf-idf":
    tf_idf_matrix = _tf_idf(doc_term_matrix)
    mean_tf_idf = tf_idf_matrix.mean(axis=0)
    return np.argsort(mean_tf_idf)[::-1][:n_features].tolist()

  if method == "count":
    mean_count = doc_term_matrix.mean(axis=0)
    return np.argsort(mean_count)[::-1][:n_features].tolist()


__all__ = [
  "get_tokenizer",
  "get_ids",
  "get_featured_ids",
]
