import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped
from posthub.db.base import Base
from posthub.db.connection import db_session
from typing import TYPE_CHECKING
from .views import UserUpdateView


if TYPE_CHECKING:
    from posthub.app.posts.models import Post


class User(Base):
    __tablename__ = 'users'

    id = sa.Column("id", sa.Integer, primary_key=True, index=True)
    username = sa.Column("username", sa.String, unique=True, nullable=False)
    password = sa.Column("password", sa.String, nullable=False)
    email_adress = sa.Column("email", sa.String, unique=True, nullable=True, default="your@example.com")
    tg_channel = sa.Column("tg_channel", sa.String, nullable=True, default="@yourtgchannel")

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    @classmethod
    async def create_user(cls, username: str, password: str, email: str, tg_channel: str):
        query = (
            sa.insert(User)
            .values(
                username=username,
                password=password,
                email=email,
                tg_channel=tg_channel,
            )
            .returning(User.id)
        )
        created_user = await db_session.get().execute(query)
        return created_user.scalars().first()

    @classmethod
    async def get_user_by_id(cls, user_id: id):
        query = (
            sa.select(User)
            .where(User.id == user_id)
        )
        user = await db_session.get().execute(query)
        return user.scalars().first()

    @classmethod
    async def get_user_by_username(cls, username: str):
        query = (
            sa.select(User)
            .where(User.username == username)
        )
        user = await db_session.get().execute(query)
        return user.scalars().first()

    @classmethod
    async def user_validation(cls, id: int, password: str):
        query = (
            sa.select(User)
            .where(
                User.id == id and User.password == password
            )
        )
        user = await db_session.get().execute(query)
        return user.scalars().first()

    @classmethod
    async def update_user_info(cls, data: UserUpdateView, user_id: int):
        query = (
            sa.update(User)
            .where(User.id == user_id)
            .values(data.dict(exclude_unset=True))
        ).returning(User)
        updated_user = await db_session.get().execute(query)
        return updated_user.scalars().first()

    @classmethod
    async def delete_user(cls, id: int):
        query = (
            sa.delete(cls)
            .where(cls.id == id)
        )
        await db_session.get().execute(query)
