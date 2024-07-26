from sequilt.model import LabelModel, RectModel, SequletModel

dummy_sequlets = [
  SequletModel(
    id=0,
    rects=[
      RectModel(value=0, x=0, y=0, width=1, height=200),
      RectModel(value=1, x=1, y=50, width=1, height=300),
      RectModel(value=2, x=2, y=0, width=1, height=200),
    ],
  ),
  SequletModel(
    id=1,
    rects=[
      RectModel(value=3, x=3, y=100, width=1, height=200),
      RectModel(value=4, x=4, y=0, width=1, height=300),
      RectModel(value=5, x=5, y=50, width=1, height=200),
    ],
  ),
  SequletModel(
    id=2,
    rects=[
      RectModel(value=6, x=2, y=450, width=1, height=200),
      RectModel(value=7, x=3, y=350, width=1, height=300),
      RectModel(value=8, x=4, y=350, width=1, height=200),
    ],
  ),
]

dummy_labels = [
  LabelModel(value=0, name="A"),
  LabelModel(value=1, name="B"),
  LabelModel(value=2, name="C"),
  LabelModel(value=3, name="D"),
  LabelModel(value=4, name="E"),
  LabelModel(value=5, name="F"),
  LabelModel(value=6, name="G"),
  LabelModel(value=7, name="H"),
  LabelModel(value=8, name="I"),
]

__all__ = ["dummy_sequlets", "dummy_labels"]
