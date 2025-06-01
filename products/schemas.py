import typing as t
from pydantic import Field, validator
from common.schemas import BaseSchema
from products.models import Product

class CreateProduct(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    description: str = Field(..., min_length=1, description="Product description")
    price: float = Field(..., gt=0, description="Product price in USD")
    image_url: t.Optional[str] = Field(None, description="Product image URL")
    is_trend: bool = Field(False, description="Whether the product is trending")
    keywords: t.Optional[str] = Field(None, max_length=500, description="Product keywords for search")
    trending_percentage: float = Field(0.0, ge=0, le=100, description="Trending percentage (0-100)")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        # Round to 2 decimal places for currency
        return round(v, 2)

    @validator('trending_percentage')
    def validate_trending_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Trending percentage must be between 0 and 100')
        # Round to 2 decimal places for percentage
        return round(v, 2)

    @validator('name', 'category')
    def validate_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()

    @validator('keywords')
    def validate_keywords(cls, v):
        if v is not None:
            # Strip whitespace and convert empty string to None
            v = v.strip()
            if not v:
                return None
            # Optional: validate keywords format (comma-separated, etc.)
            return v
        return v

class UpdateProduct(BaseSchema):
    name: t.Optional[str] = Field(None, min_length=1, max_length=255)
    category: t.Optional[str] = Field(None, min_length=1, max_length=100)
    description: t.Optional[str] = Field(None, min_length=1)
    price: t.Optional[float] = Field(None, gt=0)
    image_url: t.Optional[str] = None
    is_trend: t.Optional[bool] = None
    keywords: t.Optional[str] = Field(None, max_length=500)
    trending_percentage: t.Optional[float] = Field(None, ge=0, le=100)

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be greater than 0')
        if v is not None:
            return round(v, 2)
        return v

    @validator('trending_percentage')
    def validate_trending_percentage(cls, v):
        if v is not None:
            if v < 0 or v > 100:
                raise ValueError('Trending percentage must be between 0 and 100')
            return round(v, 2)
        return v

    @validator('name', 'category')
    def validate_strings(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('keywords')
    def validate_keywords(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                return None
            return v
        return v

class ProductResponse(Product):
    pass