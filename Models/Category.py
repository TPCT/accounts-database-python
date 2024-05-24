from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class Category(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    name: str
    sub_categories: List