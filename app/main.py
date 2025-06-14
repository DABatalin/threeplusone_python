from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.v1.router import api_router
from app.core.config import settings
from app.middleware.user_tracking import UserTrackingMiddleware
from app.core.middleware import PrometheusMiddleware
from app.services.elasticsearch import elasticsearch_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Добавляем middleware в правильном порядке
app.add_middleware(PrometheusMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(UserTrackingMiddleware)
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await elasticsearch_service.init_indices()

@app.on_event("shutdown")
async def shutdown_event():
    await elasticsearch_service.close()

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Analytics Platform"} 