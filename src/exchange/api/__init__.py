from fastapi import APIRouter

from .accountant import accountant_router
from .auth import router as auth_router
from .teller import teller_router
from .manager import manager_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(accountant_router)
router.include_router(teller_router)
router.include_router(manager_router)
