from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routes.proxy import router
from .middleware.cors import add_cors
from .middleware.waf import SimpleWAFMiddleware
from .middleware.request_id import RequestIDMiddleware

app = FastAPI(title="API Gateway", version="1.0.0")

add_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SimpleWAFMiddleware)


# Admin endpoints inline
@app.get("/api/v1/admin/users")
async def get_admin_users():
    """Get list of users for admin dashboard"""
    return [
        {
            "id": "1",
            "email": "admin@uce.edu.ec",
            "role": "admin",
            "is_verified": True,
            "is_active": True,
            "created_at": "2025-01-14T00:00:00Z"
        }
    ]


@app.patch("/api/v1/admin/users/{user_id}/role")
async def set_admin_user_role(user_id: str, payload: dict):
    """Change user role"""
    return {"ok": True, "message": f"User {user_id} role updated"}


@app.patch("/api/v1/admin/users/{user_id}/active")
async def set_admin_user_active(user_id: str, payload: dict):
    """Change user active status"""
    return {"ok": True, "message": f"User {user_id} active status updated"}


@app.get("/api/v1/admin/products")
async def get_admin_products():
    """Get list of products for admin dashboard"""
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
    """Delete a product"""
    return {"ok": True, "message": f"Product {product_id} deleted"}


app.include_router(router)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
