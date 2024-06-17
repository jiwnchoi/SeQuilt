from datasets import load_dataset

from .tokenizer import tokenizer

ds = load_dataset("LawInformedAI/overruling")


def load_overruling(truncation=True, padding="max_length", batched=True):
  ds.map(
    lambda x: tokenizer.encode(x["text"]),
    batched=True,
  )
