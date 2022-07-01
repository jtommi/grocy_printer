from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(alias="product")
    grocycode: str
    font_family: Optional[str] = None
    due_date: str
