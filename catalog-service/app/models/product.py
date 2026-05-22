from typing import Any, Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, examples=["Dell Inspiron 15"])
    category: str = Field(..., min_length=1, max_length=50, examples=["electronics"])
    price: float = Field(..., gt=0, examples=[1299.99])
    stock: int = Field(..., ge=0, examples=[15])
    attributes: dict[str, Any] = Field(
        default={},
        description="Flexible schema — varies per product category.",
        examples=[{"processor": "Intel Core i5", "ram": "8GB"}],
    )


class ProductCreate(ProductBase):
    """Request body for creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Request body for updating a product. All fields are optional."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    attributes: Optional[dict[str, Any]] = None


class ProductResponse(ProductBase):
    """Product representation returned by the API."""
    id: str = Field(..., description="MongoDB ObjectId as string")
