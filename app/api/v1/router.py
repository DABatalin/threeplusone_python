from fastapi import APIRouter

from app.api.v1.endpoints import auth, cart, comments, products, purchases, sellers, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sellers.router, prefix="/sellers", tags=["sellers"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"]) 