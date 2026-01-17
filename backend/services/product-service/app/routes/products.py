from fastapi import APIRouter, HTTPException, Query
import uuid
import json

from app.db.mongo import get_products_collection, get_audit_logs_collection
from app.db.redis import redis_client
from app.schemas.product import ProductIn, ProductOut

router = APIRouter(prefix="/api/v1/products", tags=["products"])

def cache_key(pid: str) -> str:
    return f"product:{pid}"

@router.get("/", response_model=list[ProductOut])
async def list_products(
    limit: int = Query(50, ge=1, le=200),
    status: str = Query("active"),
    seller_id: str | None = Query(None),
):
    products = get_products_collection()
    query = {} if status == "all" else {"status": status}
    if seller_id:
        query["seller_id"] = seller_id

    docs = await products.find(query).limit(limit).to_list(length=limit)
    return [
        ProductOut(id=d["_id"], **{k: v for k, v in d.items() if k != "_id"})
        for d in docs
    ]

@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductIn):
    products = get_products_collection()
    audit_logs = get_audit_logs_collection()

    _id = str(uuid.uuid4())
    doc = {"_id": _id, **payload.model_dump(), "status": "active"}
    await products.insert_one(doc)

    await audit_logs.insert_one({
        "action": "PRODUCT_CREATED",
        "product_id": _id,
        "seller_id": payload.seller_id,
    })

    await redis_client.delete(cache_key(_id))
    return ProductOut(id=_id, **payload.model_dump(), status="active")

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    products = get_products_collection()

    cached = await redis_client.get(cache_key(product_id))
    if cached:
        return ProductOut(**json.loads(cached))

    doc = await products.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(404, "Not found")

    out = ProductOut(id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"})
    await redis_client.set(cache_key(product_id), out.model_dump_json(), ex=60)
    return out

@router.patch("/{product_id}/status", response_model=ProductOut)
async def update_status(product_id: str, status: str):
    if status not in {"active", "sold", "inactive"}:
        raise HTTPException(400, "Invalid status")

    products = get_products_collection()
    audit_logs = get_audit_logs_collection()

    doc = await products.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(404, "Not found")

    await products.update_one({"_id": product_id}, {"$set": {"status": status}})
    await audit_logs.insert_one({
        "action": "PRODUCT_STATUS_UPDATED",
        "product_id": product_id,
        "status": status
    })
    await redis_client.delete(cache_key(product_id))

    doc = await products.find_one({"_id": product_id})
    return ProductOut(id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"})

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    products = get_products_collection()
    audit_logs = get_audit_logs_collection()

    doc = await products.find_one({"_id": product_id})
    if not doc:
        raise HTTPException(404, "Product not found")

    await products.delete_one({"_id": product_id})

    await audit_logs.insert_one({
        "action": "PRODUCT_DELETED",
        "product_id": product_id,
        "seller_id": doc.get("seller_id"),
    })

    await redis_client.delete(cache_key(product_id))
    return {"ok": True, "message": "Product deleted"}
