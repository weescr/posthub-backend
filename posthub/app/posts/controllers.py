from fastapi import APIRouter, Depends
from posthub.app.posts.models import Post as PostService
from posthub.app.posts import views as ValidatorsPost
from posthub.db.connection import Transaction
from posthub.protocol import Response
from posthub.auth.handlers import AuthHandler

router = APIRouter()


@router.post("/post", dependencies=[Depends(AuthHandler())])
async def create_post(data: ValidatorsPost.Post):
    async with Transaction():
        new_post = await PostService.create_post(data=data)
    data = {
        "id": new_post.id,
        "title": new_post.title,
    }
    return Response(
        message="Успешно создан новый пост",
        payload= data
    )


@router.get("/post/{id}", dependencies=[Depends(AuthHandler())])
async def get_post_by_id(id: int):
    async with Transaction():
        post = await PostService.get_post_by_id(id=id)
        
    data = {
        "title": post.title,
        "description": post.description,
        "content": post.content,
        "date": post.publication_date
    }

    return Response(
        message="Пост существует",
        payload=data
    )


@router.get("/post/title/{title}", dependencies=[Depends(AuthHandler())])
async def get_post_id_by_title(title: str):
    async with Transaction():
        post_id = await PostService.get_post_id_by_title(title=title)

    return Response(
        message="Id поста успешно получен",
        payload={
            "id": post_id
        }
    )


@router.put("/post/{id}", dependencies=[Depends(AuthHandler())])
async def update_post(id: int, data: ValidatorsPost.Post):
    async with Transaction():
        updated_post = await PostService.update_post(data=data, id=id)
    data = {
        "title": updated_post.title,
        "description": updated_post.description,
        "content": updated_post.content,
        "publication_date": updated_post.publication_date
    }
    return Response(
        message="Пост успешно обновлен",
        payload=data
    )


@router.delete("/post/{id}", dependencies=[Depends(AuthHandler())])
async def delete_post(id: int):
    async with Transaction():
        await PostService.delete_post(id=id)
    return Response(
        message="Пост успешно удален"
    )
