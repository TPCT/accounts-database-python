from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Filter(BaseModel):
    keyword: Optional[str] = None
    price_sort: Optional[str] = Field(None)

    @field_validator("price_sort")
    def check_price_sort(cls, v):
        if v not in ("asc", "desc", None):
            raise ValueError("Price sort must be either 'asc' or 'desc'")
        return v

    release_date_sort: Optional[str] = Field(None)

    @field_validator("release_date_sort")
    def check_release_date_sort(cls, v):
        if v not in ("asc", "desc", None):
            raise ValueError("Price sort must be either 'asc' or 'desc'")
        return v

    availability: Optional[bool] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    currency: Optional[str] = None

    page: Optional[int] = Field(1, ge=1)
