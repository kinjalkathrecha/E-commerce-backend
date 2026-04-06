from fastapi import APIRouter
from app.api.endpoints import (
    auth, categories, sections, products, orders, carts, 
    wishlists, addresses, reviews, promo_codes, customer_support,
    seller_applications, bulk_inquiries
)

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
api_router.include_router(promo_codes.router, prefix="/promo-codes", tags=["Promo Codes"])
api_router.include_router(customer_support.router, prefix="/support", tags=["Customer Support"])
api_router.include_router(seller_applications.router, prefix="/seller-applications", tags=["Seller Applications"])
api_router.include_router(bulk_inquiries.router, prefix="/bulk-inquiries", tags=["Bulk Inquiries"])
