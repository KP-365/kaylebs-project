"""
AI Triage RAG Agent - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import triage, health
from app.core.config import settings

app = FastAPI(
    title="AI Triage RAG Agent",
    description="A safe, local AI assistant for A&E triage",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(triage.router, prefix="/api", tags=["triage"])
app.include_router(health.router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    return {
        "message": "AI Triage RAG Agent API",
        "version": "0.1.0",
        "status": "operational"
    }


