import importlib.metadata
import os
import pathlib

import anywidget
import numpy as np
import traitlets
from IPython.display import clear_output

from seq.data import get_tf_idf_matrix, get_tokenizer, process_corpus

dev = os.environ.get("ANYWIDGET_DEV") == "1"

print(dev)
try:
  __version__ = importlib.metadata.version("seq")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"


class Widget(anywidget.AnyWidget):
  _esm = (
    pathlib.Path(__file__).parent / "static" / "widget.js"
    if not dev
    else "http://localhost:5173/widget/widget.ts?anywidget"
  )
  _css = (
    pathlib.Path(__file__).parent / "static" / "widget.css" if not dev else None
  )
  ids = traitlets.List([]).tag(sync=True)
  tokens = traitlets.List([]).tag(sync=True)
  feature_ids = traitlets.List([]).tag(sync=True)

  def __init__(
    self,
    sequences: list[str],
    max_length: int = 32,
    n_features: int = 10,
    *args,
    **kwargs,
  ) -> None:
    super().__init__(*args, **kwargs)

    self.tokenizer = get_tokenizer("nltk")
    print("Preprocessing corpus")
    corpus = process_corpus(
      sequences,
      tokenizer=self.tokenizer,
      max_tokens=max_length,
    )
    clear_output(wait=True)
    print("Processing feature elements")
    tf_idf = get_tf_idf_matrix(
      [c["ids"] for c in corpus], self.tokenizer.get_vocab_size()
    )
    self.ids = [c["ids"].tolist() for c in corpus][:300]

    mean_tf_idf = tf_idf.mean(axis=0)
    self.feature_ids = np.argsort(mean_tf_idf)[::-1][:n_features].tolist()
    clear_output(wait=True)
