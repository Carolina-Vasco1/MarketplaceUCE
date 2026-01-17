from fastapi import APIRouter, Depends, HTTPException
from app.db.mongo import get_products_collection
from app.deps.auth import require_admin

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/products")
async def admin_list_products(_admin=Depends(require_admin)):
    col = get_products_collection()
    items = await col.find({}).sort("_id", -1).to_list(length=500)

    return [
        {
            "id": str(p.get("_id")),
            "title": p.get("title", ""),
            "description": p.get("description", ""),
            "price": float(p.get("price", 0)),
            "seller_id": p.get("seller_id"),
            "image_url": p.get("image_url"),
            "status": p.get("status", "active"),
            "created_at": p.get("created_at"),
        }
        for p in items
    ]


@router.delete("/products/{product_id}")
async def admin_delete_product(product_id: str, _admin=Depends(require_admin)):
    col = get_products_collection()

    res = await col.delete_one({"_id": product_id})  # ✅ UUID string
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"ok": True}
