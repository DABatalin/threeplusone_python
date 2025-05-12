from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.services.elasticsearch import setup_elasticsearch
from app.services.sync_service import setup_elasticsearch_sync, sync_existing_data
from app.db.session import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Analytics Platform"}

@app.on_event("startup")
async def startup_event():
    # Initialize Elasticsearch indices
    setup_elasticsearch()
    
    # Setup synchronization between database and Elasticsearch
    db = SessionLocal()
    try:
        setup_elasticsearch_sync(db)
        # Sync existing data
        sync_existing_data(db)
    finally:
        db.close() 