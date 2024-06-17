from __future__ import annotations

from nltk.corpus import stopwords

from seq.data.tokenizer import tokenizer


def process_text(text: str | list[str], max_tokens: int = 16):
  if isinstance(text, list):
    tokenized = tokenizer.encode_batch(text)

    return {
      "ids": [t.ids[:max_tokens] for t in tokenized],
      "tokens": [t.tokens[:max_tokens] for t in tokenized],
    }

  else:
    tokenized = tokenizer.encode(text)

    return {
      "ids": tokenized.ids[:max_tokens],
      "tokens": tokenized.tokens[:max_tokens],
    }


__all__ = ["process_text"]
