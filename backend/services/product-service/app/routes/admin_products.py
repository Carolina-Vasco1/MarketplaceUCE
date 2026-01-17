from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.deps.auth import require_admin
from app.db.mongo import get_db

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

def _doc_to_product(d: dict) -> dict:
    return {
        "id": str(d.get("_id")),
        "title": d.get("title", ""),
        "description": d.get("description", ""),
        "price": float(d.get("price", 0)),
        "seller_id": d.get("seller_id", ""),
        "image_url": d.get("image_url"),
        "rating": float(d.get("rating", 0)),
        "review_count": int(d.get("review_count", 0)),
        "stock": int(d.get("stock", 0)),
        "created_at": d.get("created_at"),
    }

@router.get("/products")
async def admin_list_products(_admin=Depends(require_admin)):
    db = get_db()
    cursor = db["products"].find({}).sort("_id", -1)
    items = await cursor.to_list(length=500)
    return [_doc_to_product(x) for x in items]

@router.delete("/products/{product_id}")
async def admin_delete_product(product_id: str, _admin=Depends(require_admin)):
    db = get_db()

    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product id")

    res = await db["products"].delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"ok": True, "deleted": product_id}
