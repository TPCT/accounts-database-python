from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class AccountWorth(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    crowns: Optional[str] = None
    coins: Optional[str] = None
    gems: Optional[str] = None
    free: Optional[str] = None
