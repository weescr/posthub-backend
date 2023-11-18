from posthub.models.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from posthub.dto.post import Post as PostDTO
from sqlalchemy.sql import update
from sqlalchemy import delete
from sqlalchemy import select


async def create_post(data: PostDTO, db: AsyncSession):
    new_post = Post(
        title=data.title,
        description=data.description,
        content=data.content,
        publication_date=data.publication_date
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_post(id: int, db: AsyncSession):
    result = await db.execute(
        select(Post).where(Post.id == id)
    )
    post = result.scalar_one()
    return post


async def get_post_id_by_title(title: str, db: AsyncSession):
    result = await db.execute(
        select(Post.id)
        .where(
            Post.title == title
        )
    )
    post_id = result.scalar_one_or_none()
    return post_id

async def update_post(data: PostDTO, db: AsyncSession, id: int):
    async with db.begin():
        query = (
            update(Post)
            .where(Post.id == id)
            .values(data.dict(exclude_unset=True))
            .returning(Post)
        )
        updated_post = (await db.execute(query)).scalar_one()
    return updated_post


async def remove_post(db: AsyncSession, id: int):
    query = delete(Post).where(Post.id == id)
    result = await db.execute(query)
    await db.commit()
    return result
