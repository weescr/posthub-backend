from fastapi import APIRouter, Depends, HTTPException
from posthub.app.auth.models import User as UserService
from .views import (
    UserLoginView,
    UserRegistrationView,
    TokenRequestView,
    UserProfileView,
    TokenResponseView
)
from posthub.exceptions import (
    UserAlreadyRegistered,
    UserNotFoundError,
    PasswordMatchError
)
from posthub.db.connection import Transaction
from posthub.protocol import Response
from posthub.auth.handlers import decode_token, generate_tokens, AuthHandler
from posthub.auth.hash import get_password_hash

router = APIRouter()


@router.post("/user/auth/refresh_token")
async def refresh_token(body: TokenRequestView) -> Response[TokenResponseView]:
    token = decode_token(body.refresh_token)
    async with Transaction():
        user = await UserService.get_user_by_id(int(token.sub))

    if not user:
        raise UserNotFoundError

    return Response(
        message="Токен успешно обновлен",
        payload=generate_tokens(
            sub=str(user.id),
            username=user.username
        )
    )


@router.post("/user/auth/registration")
async def create_user(data: UserRegistrationView):
    async with Transaction():
        user = await UserService.get_user_by_username(username=data.username)
        if user:
            raise UserAlreadyRegistered

        user_id = await UserService.create_user(
            username=data.username,
            password=get_password_hash(data.password),
            email=data.email_adress,
            tg_channel=data.tg_channel,
        )
    return Response(
        message="Пользователь успешно создан",
        payload=generate_tokens(sub=str(user_id), username=data.username)
    )


@router.post("/user/auth/login")
async def login_user(data: UserLoginView):
    async with Transaction():
        user = await UserService.get_user_by_username(username=data.username)

    if not user:
        raise UserNotFoundError

    hashed_password = get_password_hash(data.password)
    if user.password == hashed_password:
        return Response(
            message="Вход успешно выполнен",
            payload=generate_tokens(
                sub=str(user.id),
                username=user.username,
            )
        )
    raise PasswordMatchError


@router.get("/user/profile", response_model=UserProfileView, dependencies=[Depends(AuthHandler())])
async def get_profile(current_user: str = Depends(AuthHandler())) -> UserProfileView:
    try:
        token_data = decode_token(current_user)
        user_id = token_data.sub
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
    async with Transaction():
        user_data = await UserService.get_user_by_id(int(user_id))
        if not user_data:
            raise UserNotFoundError
        return UserProfileView(username=user_data.username)



@router.delete("/user/profile", dependencies=[Depends(AuthHandler())])
async def delete_profile(current_user: str = Depends(AuthHandler())) -> Response:
    try:
        token_data = decode_token(current_user)
        user_id = int(token_data.sub)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
    async with Transaction():
        await UserService.delete_user(id=user_id)
    return Response()

