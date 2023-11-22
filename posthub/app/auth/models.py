import sqlalchemy as sa
from posthub.db.base import Base
from posthub.db.connection import db_session

from .views import UserRegistrationView, UserUpdateView


class User(Base):
    __tablename__ = 'users'

    id = sa.Column("id", sa.Integer, primary_key=True, index=True)
    username = sa.Column("username", sa.String, unique=True, nullable=False)
    password = sa.Column("password", sa.String, nullable=False)
    email_adress = sa.Column("email", sa.String, unique=True, nullable=True, default="your@example.com")
    tg_channel = sa.Column("tg_channel", sa.String, nullable=True, default="@yourtgchannel")

    @classmethod
    async def create_user(cls, data: UserRegistrationView):
        query = (
            sa.insert(User)
            .values(
                username=data.username,
                password=data.password,
                email=data.email_adress,
                tg_channel=data.tg_channel,
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
