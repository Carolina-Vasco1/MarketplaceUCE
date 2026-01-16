from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.admin_users_proxy import router as admin_users_proxy_router

from .routes.proxy import router
from .middleware.cors import add_cors
from .middleware.waf import SimpleWAFMiddleware
from .middleware.request_id import RequestIDMiddleware

app = FastAPI(title="API Gateway", version="1.0.0")

add_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SimpleWAFMiddleware)

# ✅ Admin Users: SIEMPRE por proxy (sin mock)
app.include_router(admin_users_proxy_router)

# ✅ Admin Products (si aún no tienes product-service admin real, puedes dejar mock)
@app.get("/api/v1/admin/products")
async def get_admin_products():
    return [
        {
            "id": "prod-1",
            "title": "Laptop Gaming",
            "price": 1200,
            "description": "High performance gaming laptop",
            "seller_id": "seller-1",
            "seller_name": "Vendor 1",
            "category": "Electronics",
            "rating": 4.5,
            "review_count": 10,
            "stock": 5
        },
        {
            "id": "prod-2",
            "title": "Wireless Mouse",
            "price": 35.99,
            "description": "Ergonomic wireless mouse",
            "seller_id": "seller-1",
            "seller_name": "Vendor 1",
            "category": "Accessories",
            "rating": 4.0,
            "review_count": 5,
            "stock": 20
        },
        {
            "id": "prod-3",
            "title": "USB-C Hub",
            "price": 45,
            "description": "Multi-port USB-C hub",
            "seller_id": "seller-1",
            "seller_name": "Vendor 1",
            "category": "Accessories",
            "rating": 4.2,
            "review_count": 8,
            "stock": 15
        },
        {
            "id": "prod-4",
            "title": "Mechanical Keyboard",
            "price": 150,
            "description": "RGB mechanical keyboard",
            "seller_id": "seller-1",
            "seller_name": "Vendor 1",
            "category": "Accessories",
            "rating": 4.7,
            "review_count": 15,
            "stock": 10
        }
    ]


@app.delete("/api/v1/admin/products/{product_id}")
async def delete_admin_product(product_id: str):
    return {"ok": True, "message": f"Product {product_id} deleted"}

app.include_router(router)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
