import time
import jwt

from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError


from posthub.app.auth.views import (
    AccessTokenView,
    RefreshTokenView,
    TokenResponseView,
    TokenType,
)
from posthub.exceptions import (
    JWTExpiredSignatureError,
    JWTDecodeError,
    UnauthorizedError,
)
from .hash import encode_jwt, SECRET, ALGORITHM
from posthub.config import settings


# Класс для проверки на аутентификацию пользователя в системе
class AuthHandler(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthHandler, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AuthHandler, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def get_expired_time(token_type: TokenType) -> int:
    now = datetime.now()

    if token_type == TokenType.ACCESS:
        now += settings.ACCESS_TOKEN_EXPIRES
    if token_type == TokenType.REFRESH:
        now += settings.REFRESH_TOKEN_EXPIRES

    return int(now.timestamp())


def generate_tokens(sub: str, username: str,) -> dict:
    access_token_view = AccessTokenView(
        sub=sub,
        exp=get_expired_time(token_type=TokenType.ACCESS),
        username=username,
    )
    refresh_token_view = RefreshTokenView(
        sub=sub,
        exp=get_expired_time(token_type=TokenType.REFRESH),
    )

    access_token = encode_jwt(access_token_view)
    refresh_token = encode_jwt(refresh_token_view)

    return TokenResponseView(
        access_token=access_token,
        refresh_token=refresh_token,
        exp=access_token_view.exp,
    )


def decode_token(token: str) -> RefreshTokenView:
    try:
        payload = jwt.decode(
            token, SECRET, algorithms=[ALGORITHM], options={"verify_signature": True}
        )
        if not payload:
            raise UnauthorizedError
        token_data = RefreshTokenView(**payload)
        if time.time() > token_data.exp:
            raise JWTExpiredSignatureError

    except jwt.ExpiredSignatureError as e:
        raise JWTExpiredSignatureError from e
    except jwt.DecodeError as e:
        raise JWTDecodeError from e
    except ValidationError as e:
        raise UnauthorizedError from e

    return token_data
