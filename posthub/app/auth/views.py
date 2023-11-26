from pydantic import BaseModel
from posthub.config import settings
from enum import Enum

class UserRegistrationView(BaseModel):
    username: str
    password: str
    email_adress: str
    tg_channel: str
    

class UserLoginView(BaseModel):
    username: str
    password: str


class UserUpdateView(BaseModel):
    tg_channel: str
    email_adress: str


class UserProfileView(BaseModel):
    username: str


class TokenRequestView(BaseModel):
    access_token: str
    refresh_token: str


class TokenResponseView(BaseModel):
    access_token: str
    refresh_token: str
    exp: int


class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2


class AccessTokenView(BaseModel):
    iss: str = settings.app_name
    sub: str | int
    exp: int
    username: str


class RefreshTokenView(BaseModel):
    iss: str = settings.app_name
    sub: str | int
    exp: int
