import os
from hashlib import sha256
from dotenv import load_dotenv
import jwt

from posthub.app.auth.views import AccessTokenView, RefreshTokenView

load_dotenv()
SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALG")


def get_password_hash(password: str):
    hash_pass = sha256(password.encode()).hexdigest()
    return hash_pass


def encode_jwt(payload: AccessTokenView | RefreshTokenView):
    encoded = jwt.encode(payload.dict(), SECRET, algorithm=ALGORITHM)
    return encoded
