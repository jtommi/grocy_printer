from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(alias="product")
    grocycode: str
    due_date: str
