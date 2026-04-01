"""Mock PasqOS Programs API route"""

from fastapi import APIRouter, HTTPException

from ..db import FAKE_PROGRAM_DB
from ..models import StandardResponse
from ..models.program import Program, ProgramStatus

router = APIRouter(prefix="/programs")


@router.get("/{uid}", response_model=StandardResponse[Program])
async def get_program(uid: int):
    if uid not in FAKE_PROGRAM_DB:
        # TODO: improve PasqOS error mimicking
        raise HTTPException(400, "Bad request")
    program = FAKE_PROGRAM_DB[uid]
    # TODO: Handle other cases
    program.status = ProgramStatus.RUNNING
    return StandardResponse(
        code=200,
        message="OK.",
        data=program,
    )
