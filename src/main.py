from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.logging_cfg import logger

from src.routes.gateway import router as gateway_router
from src.routes.mock_backend import router as mock_backend_router

app = FastAPI(
    title="Secure API Gateway",
    description="A lightweight secure API Gateway prototype",
    version="0.1.0"
)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    logger.info("request_received", path=request.url.path, method=request.method, client_ip=request.client.host)
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    logger.info("request_completed", path=request.url.path, status_code=response.status_code)
    return response

app.include_router(gateway_router)
app.include_router(mock_backend_router)

@app.on_event("startup")
async def startup_event():
    logger.info("gateway_starting", status="ok")
