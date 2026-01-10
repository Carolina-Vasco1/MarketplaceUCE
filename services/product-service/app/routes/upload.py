import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/products/upload", tags=["upload"])

BASE_DIR = "static/uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

os.makedirs(BASE_DIR, exist_ok=True)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only JPG, PNG or WEBP images allowed")

    ext = file.filename.split(".")[-1].lower()
    name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(BASE_DIR, name)

    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")

    with open(path, "wb") as f:
        f.write(data)

    return {"url": f"/static/uploads/{name}"}
