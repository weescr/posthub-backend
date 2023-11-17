from posthub.models.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from posthub.dto.post import Post as PostDTO
from sqlalchemy.sql import update
from sqlalchemy import delete
from sqlalchemy import select


async def create_post(data: PostDTO, db: AsyncSession):
    try:
        post = Post(
            title=data.title,
            description=data.description,
            photo=data.photo,
            video=data.video,
            publication_date=data.publication_date
        )
        async with db.begin():
            db.add(post)
            await db.commit()
            await db.refresh(post)
    except Exception as e:
        print(e)
    return post


async def get_post(id: int, db: AsyncSession):
    async with db.begin():
        result = await db.execute(
            select(Post).where(Post.id == id)
        )
        post = result.scalars().first()
    return post


async def update_post(data: PostDTO, db: AsyncSession, id: int):
    query = (
        update(Post)
        .where(Post.id == id)
        .values(data.dict(exclude_unset=True))
        .returning(Post)
    )
    updated_post = (await db.execute(query)).scalar_one()
    return updated_post


async def remove_post(db: AsyncSession, id: int):
    stmt = delete(Post).where(Post.id == id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
