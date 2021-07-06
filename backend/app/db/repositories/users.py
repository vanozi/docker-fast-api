from app.db.repositories.base import BaseRepository
from app.models.users import UserCreate, UserInDB
import uuid
from typing import List

CREATE_USER_QUERY = """
    INSERT INTO users (email, hashed_password, is_active, confirmation)
    VALUES (:email, :hashed_password, :is_active, :confirmation)
    RETURNING id, email, is_active, confirmation;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT * FROM users WHERE email = :email
"""

GET_ALL_USERS_QUERY = """
    SELECT * FROM users
"""

UPDATE_USER_QUERY = """
    UPDATE users
	SET id=:id, email=:email, confirmation=:confirmation, is_active=:is_active
	WHERE email = :email
    RETURNING *;
"""

class UsersRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """

    async def create_user(self, *, new_user: UserCreate) -> UserInDB:
        query_values = new_user.dict()
        query_values['hashed_password'] = query_values.pop('password')
        user = await self.db.fetch_one(query=CREATE_USER_QUERY, values=query_values)
        return UserInDB(**user)

    async def get_user_by_email(self, *, email:str) -> UserInDB:
        user = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email":email})
        if user is None:
            return None
        return UserInDB(**user)

    async def get_all_users(self) -> List[UserInDB]:
        users = await self.db.fetch_all(query=GET_ALL_USERS_QUERY)
        return [(UserInDB(**user) for user in users)]

    async def update_user(self, *, user: UserInDB) -> UserInDB:
        query_values = user.dict()
        updated_user = await self.db.fetch_one(query=UPDATE_USER_QUERY, values=query_values)
        return UserInDB(**updated_user)