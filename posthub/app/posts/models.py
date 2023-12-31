import sqlalchemy as sa
from posthub.db.base import Base
from posthub.db.connection import db_session
from .views import PostView as ValidatorsPost
from posthub.app.auth.models import User

class Post(Base):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, index=True)
    description = sa.Column(sa.String)
    content = sa.Column(sa.String, nullable=True)
    publication_date = sa.Column(sa.DateTime(timezone=True), server_default=sa.sql.func.now())
    user_id = sa.Column("user_id", sa.Integer, sa.ForeignKey(User.id))

    @classmethod
    async def create_post(cls, data: ValidatorsPost, owner_id: int):
        query = (
            sa.insert(Post)
            .values(
                title=data.title,
                description=data.description,
                content=data.content,
                publication_date=data.publication_date,
                user_id=owner_id
            )
            .returning(Post)
        )
        post = await db_session.get().execute(query)
        return post.scalars().first()


    @classmethod
    async def get_post_by_id(cls, id: int):
        query = sa.select(Post).where(
            Post.id == id
        )
        post = await db_session.get().execute(query)
        return post.scalars().first()

    @classmethod
    async def update_post(cls, data: ValidatorsPost, id: int):
        query = (
            sa.update(Post)
            .where(Post.id == id)
            .values(data.dict(exclude_unset=True))
        ).returning(Post)
        updated_post = await db_session.get().execute(query)
        return updated_post.scalars().first()

    @classmethod
    async def delete_post(cls, id: int):
        query = (
            sa.delete(cls).where(
                cls.id == id
            )
        )
        await db_session.get().execute(query)
