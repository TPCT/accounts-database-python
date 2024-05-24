from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemStats(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    female_clothes: Optional[int] = None
    male_clothes: Optional[int] = None
    furniture: Optional[int] = None
    floor_walls: Optional[int] = None
    apartments: Optional[int] = None
    animations: Optional[int] = None
    petkins: Optional[int] = None
    bundles: Optional[int] = None
