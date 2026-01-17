from fastapi import APIRouter, HTTPException
from app.db.mongo import get_categories_collection, get_audit_logs_collection

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/")
async def list_categories():
    categories = get_categories_collection()
    docs = await categories.find({}).sort("_id", 1).to_list(length=500)
    return [{"id": str(d["_id"]), "name": d.get("name", "")} for d in docs]

@router.post("/")
async def create_category(payload: dict):
    name = (payload.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    categories = get_categories_collection()
    audit_logs = get_audit_logs_collection()

    existing = await categories.find_one({"name": name})
    if existing:
        raise HTTPException(status_code=409, detail="Category already exists")

    res = await categories.insert_one({"name": name})

    await audit_logs.insert_one({
        "action": "CATEGORY_CREATED",
        "category_id": str(res.inserted_id),
        "name": name,
    })

    return {"id": str(res.inserted_id), "name": name}
