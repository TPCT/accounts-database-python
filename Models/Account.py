from pydantic import BaseModel, Field
from typing import Optional, List
from Core.Mongo import PyObjectId


class Account(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    account_profile_image: Optional[str] = Field(alias='account_profile_image', default=None)
    title: Optional[str] = None
    buy_now: Optional[str] = None
    account_gender: Optional[str] = Field(alias='account_gender', default=None)
