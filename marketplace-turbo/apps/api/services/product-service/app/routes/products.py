from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import json

from app.db.mongo import get_products_collection, get_audit_logs_collection
from app.db.redis import redis_client
from app.schemas.product import ProductIn, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


def cache_key(pid: str) -> str:
    return f"product:{pid}"


async def redis_get_safe(key: str) -> Optional[str]:
    try:
        return await redis_client.get(key)
    except Exception:
        return None


async def redis_set_safe(key: str, value: str, ex: int = 60) -> None:
    try:
        await redis_client.set(key, value, ex=ex)
    except Exception:
        pass


async def redis_del_safe(key: str) -> None:
    try:
        await redis_client.delete(key)
    except Exception:
        pass


def doc_to_productout(d: dict) -> ProductOut:
    """Convierte doc Mongo a ProductOut con defaults compatibles con tu schema real."""
    pid = str(d.get("_id"))
    payload = {k: v for k, v in d.items() if k != "_id"}

    # ✅ Defaults según ProductOut (ProductIn + id + status)
    payload.setdefault("title", "")
    payload.setdefault("description", "")
    payload.setdefault("price", 0.0)
    payload.setdefault("category_id", "general")
    payload.setdefault("seller_id", "")
    payload.setdefault("images", [])
    payload.setdefault("status", "active")

    # ✅ price float
    try:
        payload["price"] = float(payload.get("price", 0))
    except Exception:
        payload["price"] = 0.0

    # ✅ images lista
    imgs = payload.get("images", [])
    if imgs is None:
        imgs = []
    if not isinstance(imgs, list):
        imgs = [imgs]
    payload["images"] = imgs

    return ProductOut(id=pid, **payload)


@router.get("/", response_model=list[ProductOut])
async def list_products(
    limit: int = Query(50, ge=1, le=200),
    status: str = Query("active"),
    seller_id: Optional[str] = Query(None),
):
    col = get_products_collection()

    query = {} if status == "all" else {"status": status}
    if seller_id:
        query["seller_id"] = seller_id

    docs = await col.find(query).sort("_id", -1).limit(limit).to_list(length=limit)
    return [doc_to_productout(d) for d in docs]


@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductIn):
    col = get_products_collection()
    audit = get_audit_logs_collection()

    _id = str(uuid.uuid4())
    doc = {"_id": _id, **payload.model_dump(), "status": "active"}

    await col.insert_one(doc)

    await audit.insert_one(
        {
            "action": "PRODUCT_CREATED",
            "product_id": _id,
            "seller_id": doc.get("seller_id"),
        }
    )

    await redis_del_safe(cache_key(_id))
    return ProductOut(id=_id, **payload.model_dump(), status="active")


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    col = get_products_collection()

    cached = await redis_get_safe(cache_key(product_id))
    if cached:
        return ProductOut(**json.loads(cached))

    doc = await col.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")

    out = doc_to_productout(doc)
    await redis_set_safe(cache_key(product_id), out.model_dump_json(), ex=60)
    return out


# -----------------------------
# ✅ NUEVO: PATCH para EDITAR PRODUCTO (title/description/price/category_id/images)
# -----------------------------
class ProductUpdateIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category_id: Optional[str] = None
    images: Optional[List[str]] = None


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, body: ProductUpdateIn):
    col = get_products_collection()
    audit = get_audit_logs_collection()

    doc = await col.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")

    data = body.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # ✅ normaliza images
    if "images" in data:
        if data["images"] is None:
            data["images"] = []
        if not isinstance(data["images"], list):
            data["images"] = [data["images"]]

    await col.update_one({"_id": product_id}, {"$set": data})

    await audit.insert_one(
        {
            "action": "PRODUCT_UPDATED",
            "product_id": product_id,
            "seller_id": doc.get("seller_id"),
            "updated_fields": list(data.keys()),
        }
    )

    await redis_del_safe(cache_key(product_id))

    doc2 = await col.find_one({"_id": product_id})
    return doc_to_productout(doc2)


class UpdateStatusIn(BaseModel):
    status: str


@router.patch("/{product_id}/status", response_model=ProductOut)
async def update_status(product_id: str, body: UpdateStatusIn):
    if body.status not in {"active", "sold", "inactive"}:
        raise HTTPException(status_code=400, detail="Invalid status")

    col = get_products_collection()
    audit = get_audit_logs_collection()

    doc = await col.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")

    await col.update_one({"_id": product_id}, {"$set": {"status": body.status}})

    await audit.insert_one(
        {
            "action": "PRODUCT_STATUS_UPDATED",
            "product_id": product_id,
            "status": body.status,
        }
    )

    await redis_del_safe(cache_key(product_id))

    doc2 = await col.find_one({"_id": product_id})
    return doc_to_productout(doc2)


@router.delete("/{product_id}")
@router.delete("/{product_id}/")
async def delete_product(product_id: str):
    col = get_products_collection()
    audit = get_audit_logs_collection()

    doc = await col.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")

    await col.delete_one({"_id": product_id})

    await audit.insert_one(
        {
            "action": "PRODUCT_DELETED",
            "product_id": product_id,
            "seller_id": doc.get("seller_id"),
        }
    )

    await redis_del_safe(cache_key(product_id))
    return {"ok": True, "message": "Product deleted"}
