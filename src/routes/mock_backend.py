from fastapi import APIRouter, Depends, Request
from src.auth import get_current_user
from src.models import TokenData, DataPayload
from src.limiter import limiter
from src.logging_cfg import logger

router = APIRouter(prefix="/api")

@router.get("/protected")
@limiter.limit("20/minute")
async def get_protected_data(request: Request, current_user: TokenData = Depends(get_current_user)):
    return {"msg": f"Hello {current_user.username}", "data": "This is protected data"}

@router.post("/data")
@limiter.limit("10/minute")
async def post_data(request: Request, payload: DataPayload, current_user: TokenData = Depends(get_current_user)):
    logger.info("data_payload_accepted", user=current_user.username, payload_id=payload.id)
    return {
        "status": "success",
        "processed_payload": payload.model_dump(),
        "X-Gateway-Processed": True
    }
