import time
import psutil
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.metrics import REQUEST_TIME, REQUEST_COUNT, ERROR_COUNT, MEMORY_USAGE, APP_INFO
from app.core.config import settings

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        process = psutil.Process()
        MEMORY_USAGE.set(process.memory_info().rss)
        
        APP_INFO.info({
            "version": "1.0.0",
            "app_name": settings.PROJECT_NAME
        })
        
        try:
            response = await call_next(request)
            
            if not request.url.path.startswith("/metrics"):
                REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    status_code=response.status_code
                ).inc()
                
                REQUEST_TIME.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    status_code=response.status_code
                ).observe(time.time() - start_time)
            
            return response
            
        except Exception as exc:
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=500,
                error_type=type(exc).__name__
            ).inc()
            raise 