from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.users import UserCreate, UserPublic
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.utils.auth import Auth
from jose import jwt
from app.core import config


router = APIRouter()


@router.get("/activate_email/{token}")
async def activate_email(
    token: str, users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPublic:
    invalid_token_error = HTTPException(status_code=400, detail="Invalid token")
    # Check if token expiration date is reached
    try:
        payload = jwt.decode(token, str(config.SECRET_KEY), algorithms=config.ALGORITHM)
    except jwt.JWTError as e:
        print(e)
        raise HTTPException(status_code=403, detail="Token has expired")
    # Check if scope of the token is valid
    if payload["scope"] != "registration":
        raise invalid_token_error
    user = await users_repo.get_user_by_email(email=payload["sub"])
    # Check if token belongs to user and not already been used
    if not user or user.confirmation is None or user.confirmation.hex != payload["jti"]:
        raise invalid_token_error
    if user.is_active:
        raise HTTPException(status_code=403, detail="User already activated")
    # Set confirmation UID to None and user to active
    user.confirmation = None
    user.is_active = True
    updated_user = await users_repo.update_user(user=user)
    return updated_user


@router.post("/access_token")
async def get_access_token(users_repo: UsersRepository = Depends(get_repository(UsersRepository), OAuth2PasswordRequestForm = Depends())



# @router.post("/token", response_model=Token)
# async def login_for_access_token(settings: config.Settings = Depends(get_settings), db: Session = Depends(get_db),
#                                  form_data: OAuth2PasswordRequestForm = Depends()):
#     user = Auth.authenticate_user(db=db, email=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
#     access_token = Auth.create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires, settings=settings
#     )
#     return {"access_token": access_token, "token_type": "bearer"}