from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.expense_routes import router as expense_router
from routes.receipt_routes import router as receipt_router
from routes.analytics_routes import router as analytics_router
from routes.dashboard_routes import router as dashboard_router

app = FastAPI(
    title="FinSight AI API",
    description="Backend API for AI-powered expense tracking from receipts.",
    version="1.0.0",
)

import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
       "https://fin-sight-ai-frontend-liard.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/api",
    tags=["Authentication"],
)
app.include_router(
    dashboard_router,
    prefix="/api",
    tags=["Dashboard"],
)

app.include_router(
    expense_router,
    prefix="/api",
    tags=["Expenses"],
)

app.include_router(
    receipt_router,
    prefix="/api",
    tags=["Receipts"],
)

app.include_router(
    analytics_router,
    prefix="/api",
    tags=["Analytics"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to FinSight AI API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }