from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

import posthub.app.healthcheck.controllers as healthcheck
from posthub import exceptions
from posthub.db import get_session
from posthub.logger import logger
from posthub.protocol import Response
from posthub.postManager import ManagerPost
import requests

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

config = {
    'ACCESS_TOKEN': "",
    'GROUP_ID': -96514621,
    'VERSION': 5.199
}



@app.post("/vk/post")
async def publish_post(comment: str, day: str, time: str):
    post_manager = ManagerPost(config)
    post_manager.CommitPost(Comment=comment, Day=day, Time=time)

    print(f"Сообщение отправлено: {comment}")
    return {'success': True}


@app.post("/vk/getUserToken")
async def get_user_token(access_token: str):
    return "success"


@app.post("vk/getUserGroups")
async def get_user_groups(user_id: str):
    return


@app.get("vk/auth")
async def auth_user():
    response = requests.get("https://oauth.vk.com/authorize?",
                            params={"client_id": CLIENT_ID,
                                    "redirect_url": "https://oauth.vk.com/blank.html",
                                    "scope": "wall,groups",
                                    "response_type": "token",
                                    "v": 5.199})
    print(response.json())


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

    uvicorn.run("main:app", host="0.0.0.0", port=5000)
