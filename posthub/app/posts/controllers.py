from telegram import Bot
from fastapi import APIRouter, Depends
from posthub.app.posts.models import Post as PostService
from posthub.app.auth.models import User
from posthub.app.posts import views as ValidatorsPost
from posthub.db.connection import Transaction
from posthub.protocol import Response
from posthub.auth.handlers import AuthHandler
from posthub.auth.handlers import decode_token
from posthub.exceptions import UnauthorizedError, SocialTokenError
from posthub.posts.post import post_to_telegram, post_to_vk
router = APIRouter()


@router.post("/post", dependencies=[Depends(AuthHandler())])
async def create_post(data: ValidatorsPost.PostView, current_user: int = Depends(AuthHandler())):
    async with Transaction():
        # Айдишник юзера
        usr_id = int(decode_token(current_user).sub)
        # Данные о пользователе
        vk_token = await User.get_vk_token(user_id=usr_id)
        tgbot_token = await User.get_tgbot_token(user_id=usr_id)
        tg_channel = await User.get_tgchannel(user_id=usr_id)
        if vk_token is not None and tgbot_token is not None and tg_channel is not None:
           await post_to_vk(
               vk_token=vk_token, 
               title=data.title, 
               description=data.description,
               content=data.content
               )
           await post_to_telegram(
               tgbot_token=tgbot_token,
               tg_channel=tg_channel,
               title=data.title,
               description=data.description,
               content=data.content
           )
        else:
            raise SocialTokenError

        new_post = await PostService.create_post(data=data, owner_id=usr_id)

    return Response(
        message="Успешно создан новый пост",
        payload=ValidatorsPost.PostView.from_orm(new_post)
    )


@router.get("/post/{id}", dependencies=[Depends(AuthHandler())])
async def get_post_by_id(id: int, current_user: int = Depends(AuthHandler())):
    async with Transaction():
        post = await PostService.get_post_by_id(id=id)
        owner_id = int(decode_token(current_user).sub)
        if (post.user_id == owner_id) and (post.user_id is not None):
            return Response(
                message="Пост существует",
                payload=ValidatorsPost.PostView.from_orm(post)
            )
        raise UnauthorizedError


@router.put("/post/{id}", dependencies=[Depends(AuthHandler())])
async def update_post(id: int, data: ValidatorsPost.PostView, current_user: int = Depends(AuthHandler())):
    async with Transaction():
        updated_post = await PostService.update_post(data=data, id=id)
        owner_id = int(decode_token(current_user).sub)
        if updated_post.user_id == owner_id:
            return Response(
                message="Пост успешно обновлен",
                payload=ValidatorsPost.PostView.from_orm(updated_post)
            )
        raise UnauthorizedError


@router.delete("/post/{id}", dependencies=[Depends(AuthHandler())])
async def delete_post(id: int, current_user: int = Depends(AuthHandler())):
    async with Transaction():
        owner_id = int(decode_token(current_user).sub)
        post = await PostService.get_post_by_id(id=id)
        if post.user_id == owner_id:
            await PostService.delete_post(id=id)
            return Response(
                message="Пост успешно удален"
            )
        else:
            raise UnauthorizedError
