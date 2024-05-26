from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class Profile(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    username:  Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    age_verification_account_status: Optional[str] = None
    date_created: Optional[datetime] = None
