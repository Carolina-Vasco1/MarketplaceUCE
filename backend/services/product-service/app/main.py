from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from .routes.products import router as products_router
from .routes.categories import router as categories_router
from .routes.upload import router as upload_router

app = FastAPI(title="Product Service", version="1.0.0")

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(upload_router)

# ✅ servir imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
