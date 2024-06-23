from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from Models.Item import Item


class Items(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    items: List[Item]
    pages: int
