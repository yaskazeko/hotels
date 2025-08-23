from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemes.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["authentication and authorization"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        data: UserRequestAdd,

):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(username=data.username, email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:

        if await UsersRepository(session).get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}
