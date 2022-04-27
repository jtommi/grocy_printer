from datetime import datetime
from typing import Optional

import pendulum
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(alias="product")
    grocycode: str
    font_family: Optional[str] = None
    due_date: str
    creation_date: Optional[datetime] = pendulum.now("Europe/Brussels")
