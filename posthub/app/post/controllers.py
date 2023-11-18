from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from posthub.db import get_session

from posthub.services import post as PostService
from posthub.dto import post as PostDTO

router = APIRouter()


@router.post("/post")
async def create_post(db: AsyncSession = Depends(get_session), data: PostDTO.Post = None):
    return await PostService.create_post(data=data, db=db)


@router.get("/post/{id}")
async def get_post(db: AsyncSession = Depends(get_session), id: int = None):
    return await PostService.get_post(id=id, db=db)


@router.get("/post/title/{title}")
async def get_post_id_by_title(title: str, db: AsyncSession = Depends(get_session)):
    return await PostService.get_post_id_by_title(title=title, db=db)


@router.put("/post/{id}")
async def update_post(id: int, db: AsyncSession = Depends(get_session), data: PostDTO.Post = None):
    return await PostService.update_post(data=data, db=db, id=id)


@router.delete("/post/{id}")
async def delete_post(db: AsyncSession = Depends(get_session), id: int = None):
    return await PostService.remove_post(db=db, id=id)
