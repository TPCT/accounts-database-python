from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class Xp(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    name: str
    level: Optional[int] = None
    level_xp: Optional[int] = None
