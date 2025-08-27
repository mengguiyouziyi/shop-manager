from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Any, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

async def general_exception_handler(request: Any, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"}
    )

class ShopManagerException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def raise_http_exception(message: str, status_code: int = 400):
    raise HTTPException(status_code=status_code, detail=message)