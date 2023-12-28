import sqlalchemy as sa
from posthub.db.base import Base
from posthub.db.connection import db_session

class User(Base):
    __tablename__ = 'users'

    id = sa.Column("id", sa.Integer, primary_key=True, index=True)
    username = sa.Column("username", sa.String, unique=True, nullable=False)
    password = sa.Column("password", sa.String, nullable=False)
    email_adress = sa.Column("email", sa.String, unique=True, nullable=True, default="your@example.com")
    tg_channel = sa.Column("tg_channel", sa.String, nullable=True,
                           default="@yourtgchannel", server_default="@yourtgchannel")
    vk_token = sa.Column("vk_token", sa.String, nullable=True)
    tg_bot_token = sa.Column("tg_bot_token", sa.String, nullable=True)

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
    async def delete_user(cls, id: int):
        query = (
            sa.delete(cls)
            .where(cls.id == id)
        )
        await db_session.get().execute(query)

    @classmethod
    async def update_vk_token(cls, vk_token: str, user_id: int):
        query = (
            sa.update(User)
            .where(User.id == user_id)
            .values(
                vk_token=vk_token
            )
            .returning(User.vk_token)
        )
        upd_token = await db_session.get().execute(query)
        return upd_token.scalars().first()

    @classmethod
    async def update_tg_bot_token(cls, tg_bot_token: str, user_id: int):
        query = (
            sa.update(User)
            .where(User.id == user_id)
            .values(
                tg_bot_token=tg_bot_token
            )
            .returning(User.tg_bot_token)
        )
        upd_token = await db_session.get().execute(query)
        return upd_token.scalars().first()
    
    @classmethod
    async def get_vk_token(cls, user_id: int):
        query = (
            sa.select(User.vk_token).where(User.id == user_id)
        )
        vk_token = await db_session.get().execute(query)
        return vk_token.scalars().first()
    
    @classmethod
    async def get_tgbot_token(cls, user_id: int):
        query = (
            sa.select(User.tg_bot_token).where(User.id == user_id)
        )
        vk_token = await db_session.get().execute(query)
        return vk_token.scalars().first()
    
    @classmethod
    async def get_tgchannel(cls, user_id: int):
        query = (
            sa.select(User.tg_channel).where(User.id == user_id)
        )
        vk_token = await db_session.get().execute(query)
        return vk_token.scalars().first()

