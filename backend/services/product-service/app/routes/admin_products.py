from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.deps.auth import require_admin
from app.db.mongo import get_products_collection

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/products")
async def admin_list_products(_admin=Depends(require_admin)):
    products_col = get_products_collection()

    cursor = products_col.find({}).sort("_id", -1)
    items = await cursor.to_list(length=500)

    return [
        {
            "id": str(p["_id"]),
            "title": p.get("title"),
            "description": p.get("description"),
            "price": float(p.get("price", 0)),
            "seller_id": p.get("seller_id"),
            "image_url": p.get("image_url"),
            "stock": p.get("stock", 0),
            "created_at": p.get("created_at"),
        }
        for p in items
    ]


@router.delete("/products/{product_id}")
async def admin_delete_product(
    product_id: str,
    _admin=Depends(require_admin),
):
    products_col = get_products_collection()

    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product id")

    res = await products_col.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"ok": True}
