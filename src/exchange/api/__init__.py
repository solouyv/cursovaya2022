from fastapi import APIRouter

from .exchange import router as exchange_router
from .accountant import accountant_router
from .teller import teller_router

router = APIRouter()
router.include_router(exchange_router)
router.include_router(accountant_router)
router.include_router(teller_router)
