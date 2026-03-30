from fastapi import APIRouter
from app.api.endpoints import auth, categories, sections, products, orders, carts, wishlists, addresses, reviews

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(sections.router, prefix="/sections", tags=["Sections"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(carts.router, prefix="/cart", tags=["Cart"])
api_router.include_router(wishlists.router, prefix="/wishlist", tags=["Wishlist"])
api_router.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
