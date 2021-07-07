from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.users import UserCreate, UserPublic, UserInDB
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.utils.auth import Auth
from app.utils.mailer import Mailer

from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_all_users(current_user: UserInDB = Depends(get_current_user),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> List[UserPublic]:
    users = await users_repo.get_all_users()
    return users


@router.post(
    "/",
    response_model=UserPublic,
    name="users:create-user",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(
    new_user: UserCreate = Body(..., embed=True),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    # Check if user with email allready exists
    user = await users_repo.get_user_by_email(email=new_user.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    confirmation = Auth.create_confirmation_token(email=new_user.email)
    # Try to send an email with the email confimation link
    try:
        Mailer.send_confirmation_message(confirmation["token"], new_user.email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email couldn't be send. Please try again.",
        )
    # Create new user
    new_user.password = Auth.create_password_hash(password=new_user.password)
    new_user.confirmation = confirmation["jti"]
    created_user = await users_repo.create_user(new_user=new_user)
    # Debug print token
    print(confirmation)
    return created_user
