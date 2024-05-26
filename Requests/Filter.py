from pydantic import BaseModel, Field, field_validator
from typing import Optional
from fastapi.exceptions import RequestValidationError


class Filter(BaseModel):
    keyword: Optional[str] = None
    price_sort: Optional[str] = Field(None)

    @field_validator("price_sort")
    def check_price_sort(cls, v):
        if v not in ("asc", "desc", None):
            raise RequestValidationError("Price sort must be either 'asc' or 'desc'")
        return v

    release_date_sort: Optional[str] = Field(None)

    @field_validator("release_date_sort")
    def check_release_date_sort(cls, v):
        if v not in ("asc", "desc", None):
            raise RequestValidationError("Price sort must be either 'asc' or 'desc'")
        return v

    availability: Optional[bool] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    currency: Optional[str] = None

    @field_validator('currency')
    def check_currency(cls, v):
        if v not in ("Crowns", "Gems", "Coins", "Free", None):
            raise RequestValidationError("Currency must be either 'Crowns', 'Gems', 'Coins', 'Free'")
        return v

    page: Optional[int] = Field(1, ge=1)
