from fastapi import APIRouter

from posthub.protocol import Response

router = APIRouter()


@router.get(
    "/healthz",
    response_model=Response,
)
async def get_healthcheck():
    return Response()
