from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

import posthub.app.healthcheck.controllers as healthcheck
from posthub.app.posts import controllers as PostControllers
from posthub import exceptions
from posthub.db import get_session
from posthub.logger import logger
from posthub.protocol import Response

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    dependencies=[Depends(get_session)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router, tags=["healthcheck"])
app.include_router(PostControllers.router, tags=["post"])


@app.exception_handler(Exception)
async def uvicorn_base_exception_handler(request: Request, exc: Exception):
    logger.debug(exc)
    error = exceptions.ServerError(debug=str(exc))
    return ORJSONResponse(
        Response(
            code=error.status_code, message=error.message, body=error.payload
        ).dict()
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(request: Request, exc: exceptions.ApiException):
    logger.debug(exc.debug)

    return ORJSONResponse(
        Response(
            code=exc.status_code,
            message=exc.message,
            body=exc.payload,
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=5000)
