from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository
from app.core import config
import uuid

from app.models.users import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/access_token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_password_hash(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, str(config.SECRET_KEY), algorithm=config.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def create_access_token(email: str):
        jti = uuid.uuid4().hex
        claims = {"sub": email, "scope": "login", "jti": jti}
        return Auth.create_jwt_token(
            claims,
            timedelta(minutes=config.ACCESS_TOKEN_LIFETIME),
        )

    @staticmethod
    def create_confirmation_token(email: str):
        jti = uuid.uuid4().hex
        claims = {"sub": email, "scope": "registration", "jti": jti}
        return {
            "jti": jti,
            "token": Auth.create_jwt_token(
                claims,
                timedelta(minutes=config.REGISTRATION_TOKEN_LIFETIME),
            ),
        }

    @staticmethod
    def create_password_reset_token(user_email: str):
        jti = uuid.uuid4()
        claims = {"sub": user_email, "scope": "password_reset", "jti": jti.hex}
        return {
            "jti": jti,
            "token": Auth.create_access_token(
                claims,
                settings,
                timedelta(minutes=settings.reset_password_token_lifetime),
            ),
        }

    # Authenticate and return user
    @staticmethod
    async def authenticate_user(
        email: str,
        password: str,
        users_repo: UsersRepository
    ):
        user = await users_repo.get_user_by_email(email=email)
        if not user:
            return False
        if not Auth.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return False
        return user



# get current user
async def get_current_user(users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
                           token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(config.SECRET_KEY), algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exceptions
    user = users_repo.get_user_by_email(email=usernametoken_data.username)
    if user is None:
        raise credentials_exception
    return user


# get current active use
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
