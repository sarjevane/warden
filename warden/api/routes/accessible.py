from logging import getLogger

from fastapi import APIRouter, Depends

from warden.api.routes.dependencies.auth import verify_root
from warden.api.schemas.accessible import AccessibleResponse

logger = getLogger(__name__)
router = APIRouter(prefix="/accessible")


@router.get("")
async def is_accessible(
    _=Depends(verify_root),
) -> AccessibleResponse:
    """Warden endpoint for qrmi 'is_accessible' interface"""
    # TODO: implement logic for blocking qrmi access to pasqal_local here
    return AccessibleResponse(is_accessible=True, message="Warden ok.")
