from __future__ import annotations

from datasets import load_dataset

from seq.data.process import process_text


def load_overruling(max_tokens: int = 16):
  ds = load_dataset("LawInformedAI/overruling")
  return ds.map(
    lambda x: process_text(text=x["sentence1"], max_tokens=max_tokens),
    batched=True,
  )


if __name__ == "__main__":
  print(load_overruling())

__all__ = ["load_overruling"]
