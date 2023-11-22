from fastapi import APIRouter
from posthub.app.auth.models import User as UserService
from .views import UserLoginView, UserRegistrationView, UserUpdateView, UserGetProfileView
from posthub.db.connection import Transaction
from posthub.protocol import Response
from posthub.exceptions import UserAlreadyRegistered, UserNotFoundError, PasswordMatchError


router = APIRouter()


@router.post("/user/auth/registration")
async def create_user(data: UserRegistrationView):
    async with Transaction():
        user = await UserService.get_user_by_username(username=data.username)
        if user:
            raise UserAlreadyRegistered

        user_id = await UserService.create_user(data=data)
    return Response(
        message="Пользователь успешно создан",
        payload={'user_id': user_id, 'username': data.username}
    )


@router.put("/user/update_profile/{id}")
async def update_user_data(data: UserUpdateView, id: int):
    async with Transaction():
        check_user = await UserService.get_user_by_id(user_id=id)

        if not check_user:
            raise UserNotFoundError

        updated_user = await UserService.update_user_info(data=data, user_id=id)
        updated_payload = {
            "tg_channel": updated_user.tg_channel,
            "email": updated_user.email_adress
        }
    return Response(
        message="Информация о пользователе обновлена",
        payload=updated_payload
    )


@router.post("/user/auth/login")
async def login_user(data: UserLoginView):
    async with Transaction():
        user = await UserService.get_user_by_username(username=data.username)
    if not user:
        raise UserNotFoundError

    if user.password == data.password:
        return Response(
            message="Авторизация успешна!",
            payload={
                "username": user.username
            }
        )
    raise PasswordMatchError


@router.post("/user/profile")
async def get_profile(data: UserGetProfileView):
    async with Transaction():
        user = await UserService.get_user_by_username(data.username)
        if not user:
            raise UserNotFoundError

        return Response(
            message="Профиль существует!",
            payload={
                "username": user.username,
                "tg_channel": user.tg_channel,
                "email": user.email_adress
            }
        )


@router.delete("/user/profile")
async def delete_profile(id: int):
    async with Transaction():
        await UserService.delete_user(id=id)
    return Response()
