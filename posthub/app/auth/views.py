from pydantic import BaseModel


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


class UserGetProfileView(BaseModel):
    username: str