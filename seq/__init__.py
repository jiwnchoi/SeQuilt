import importlib.metadata
import os
import pathlib

import anywidget
import traitlets

dev = os.environ.get("ANYWIDGET_DEV") == "1"


try:
  __version__ = importlib.metadata.version("seq")
except importlib.metadata.PackageNotFoundError:
  __version__ = "unknown"


class Widget(anywidget.AnyWidget):
  _esm = (
    pathlib.Path(__file__).parent / "static" / "seq.js"
    if not dev
    else "http://localhost:5173/widget/widget.ts?anywidget"
  )
  _css = (
    pathlib.Path(__file__).parent / "static" / "style.css" if not dev else None
  )
  value = traitlets.Int(0).tag(sync=True)
