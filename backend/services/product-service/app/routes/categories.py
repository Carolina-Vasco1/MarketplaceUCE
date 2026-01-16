import uuid
from fastapi import APIRouter, HTTPException
from ..db.mongo import categories, audit_logs
from ..schemas.category import CategoryIn, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryOut)
async def create_category(payload: CategoryIn):
    _id = str(uuid.uuid4())
    await categories.insert_one({"_id": _id, "name": payload.name})
    await audit_logs.insert_one({"action": "CATEGORY_CREATED", "category_id": _id})
    return CategoryOut(id=_id, name=payload.name)

@router.get("/", response_model=list[CategoryOut])
async def list_categories():
    out: list[CategoryOut] = []
    async for doc in categories.find({}):
        out.append(CategoryOut(id=doc["_id"], name=doc["name"]))
    return out

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: str):
    doc = await categories.find_one({"_id": category_id})
    if not doc:
        raise HTTPException(404, "Not found")
    return CategoryOut(id=doc["_id"], name=doc["name"])
