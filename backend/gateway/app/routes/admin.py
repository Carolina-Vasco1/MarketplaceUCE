from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..core.rbac import require_roles

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
@require_roles("admin")
async def get_admin_users(current_user: dict = Depends(get_current_user)):
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


@router.get("/products")
@require_roles("admin")
async def get_admin_products(current_user: dict = Depends(get_current_user)):
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


@router.get("/dashboard")
@require_roles("admin")
async def get_admin_dashboard(current_user: dict = Depends(get_current_user)):
    """Get dashboard stats for admin"""
    return {
        "stats": {
            "total_users": 1,
            "total_products": 4,
            "total_orders": 0,
            "total_revenue": 0
        }
    }
