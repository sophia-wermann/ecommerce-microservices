from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Query, status
from app.database import get_database
from app.models.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


def _serialize(doc: dict) -> dict:
    """Convert MongoDB document to API-friendly dict (ObjectId → string id)."""
    doc["id"] = str(doc.pop("_id"))
    return doc


def _collection():
    return get_database()["products"]


def _parse_object_id(product_id: str) -> ObjectId:
    try:
        return ObjectId(product_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{product_id}' is not a valid product ID.",
        )


# ── GET /products ──────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="List products",
    description="Returns all products. Filter by category using the `?category=` query parameter.",
)
async def list_products(
    category: Optional[str] = Query(default=None, description="Filter by category (e.g. electronics, clothing)"),
    limit: int = Query(default=100, ge=1, le=500, description="Maximum number of results"),
):
    query = {"category": category} if category else {}
    docs = await _collection().find(query).to_list(length=limit)
    return [_serialize(doc) for doc in docs]


# ── GET /products/{id} ─────────────────────────────────────────────────────────

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
)
async def get_product(product_id: str):
    doc = await _collection().find_one({"_id": _parse_object_id(product_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return _serialize(doc)


# ── POST /products ─────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
)
async def create_product(product: ProductCreate):
    result = await _collection().insert_one(product.model_dump())
    created = await _collection().find_one({"_id": result.inserted_id})
    return _serialize(created)


# ── PUT /products/{id} ─────────────────────────────────────────────────────────

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
)
async def update_product(product_id: str, product: ProductUpdate):
    update_data = {k: v for k, v in product.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update.",
        )

    oid = _parse_object_id(product_id)
    result = await _collection().update_one({"_id": oid}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    updated = await _collection().find_one({"_id": oid})
    return _serialize(updated)


# ── DELETE /products/{id} ──────────────────────────────────────────────────────

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
)
async def delete_product(product_id: str):
    result = await _collection().delete_one({"_id": _parse_object_id(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
