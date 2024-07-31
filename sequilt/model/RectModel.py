from pydantic import BaseModel


class RectModel(BaseModel):
  value: int
  x: int
  y: int
  width: int
  height: int
