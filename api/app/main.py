from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import pricing

app = FastAPI(
    title="Option Pricing API",
    description="Simple API for calculating option prices using Black-Scholes, Binomial, and Trinomial models",
    version="1.0.0",
)

# CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include pricing router
app.include_router(pricing.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Option Pricing API is running",
        "endpoint": "/api/calculate",
    }
