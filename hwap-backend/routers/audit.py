"""Audit router."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api")

@router.get("/audit")
async def get_audit(search: str = "", filter: str = ""):
    return [
        {
            "time": datetime.utcnow().isoformat(),
            "user": "system",
            "op": "startup",
            "algo": "none",
            "result": "success"
        }
    ]
