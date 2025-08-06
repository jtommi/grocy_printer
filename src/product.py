from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(alias="product", title="The name of the product.")
    grocycode: str = Field(title="The Grocy code of the product.")
    due_date: str = Field(title="The due date of the product.")
