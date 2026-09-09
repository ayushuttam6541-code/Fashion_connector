from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import init_db, close_db
from routes import auth, shops, products, admin, wishlist, cart, orders, categories, contact
import os

# Initialize FastAPI app
app = FastAPI(
    title="FashionConnect API",
    description="Hyperlocal Fashion Marketplace for Patna, Bihar",
    version="2.0.0"
)

# CORS configuration
frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(auth.router, prefix="/api")
app.include_router(shops.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(wishlist.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(contact.router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FashionConnect API"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FashionConnect API - Hyperlocal Fashion Marketplace",
        "version": "2.0.0",
        "docs": "/docs"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    await init_db()
    print("FashionConnect API started successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("FashionConnect API shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)