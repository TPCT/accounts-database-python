from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class Xp(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    name: str
    xp: Optional[int] = None
    level: Optional[int] = None
    level_xp: Optional[int] = None
    next_level: Optional[int] = None
    next_level_xp: Optional[int] = None
    leveled_up: Optional[int] = None