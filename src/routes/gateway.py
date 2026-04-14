from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import create_access_token, get_current_active_admin, verify_password, get_password_hash
from src.models import Token
from src.logging_cfg import logger
from src.limiter import limiter
from typing import Any

router = APIRouter()

# Mock user db for prototype - passwords are 'admin123' and 'user123'
MOCK_USERS = {
    "admin": {"password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", "role": "admin"},
    "user": {"password_hash": "$2b$12$xGzTItQ72vJ7W2oE.4N5HuwE1U1A3L/mYg5R.uR0s5EIfIuQGZZp6", "role": "user"}
}

@router.post("/auth/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        logger.warning("auth_failed_invalid_credentials", username=form_data.username, type="security_event", ip=request.client.host)
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username, "role": user["role"]})
    logger.info("auth_success", username=form_data.username, ip=request.client.host)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/gateway/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {"status": "ok"}

@router.get("/gateway/logs")
@limiter.limit("5/minute")
async def get_logs(request: Request, current_admin: Any = Depends(get_current_active_admin)):
    return {"msg": "Logs access successful", "role": current_admin.role}
