from pydantic import BaseModel


class LabelModel(BaseModel):
  value: int
  name: str
