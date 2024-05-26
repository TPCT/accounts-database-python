from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime


class Item(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    price: Optional[int]
    name: Optional[str]
    category: Optional[str]
    thumbnail_url: Optional[str]
    currency: Optional[str]
    mock_id: Optional[str]
    hidden: Optional[bool]
    release_date: Optional[datetime]
    sub_category: Optional[str]