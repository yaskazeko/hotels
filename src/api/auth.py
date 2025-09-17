
from typing import Annotated

from fastapi import APIRouter, Cookie, HTTPException, Request, Response

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemes.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["authentication and authorization"])

@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_is": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"logout": "Ok"}


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(username=data.username, email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:

        if await UsersRepository(session).get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}

@router.get("/only_auth")
async def only_auth(

        request: Request,
        access_token: Annotated[str | None, Cookie()] = None,
):

    async with async_session_maker() as session:

        if access_token is None:
            raise HTTPException(status_code=401, detail="Access token required or expired")

    return {
        "authorised": "Pass",
        "access_token": access_token
    }
