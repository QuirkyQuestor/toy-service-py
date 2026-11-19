from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    name: str = Field(min_length=1)


class Item(ItemIn):
    id: int
