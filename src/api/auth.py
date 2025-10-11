
from typing import Annotated

from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from src.api.dependencies import DBDep
from src.repositories.users import UsersRepository
from src.schemes.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["authentication and authorization"])

@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
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
        db: DBDep,
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(username=data.username, email=data.email, hashed_password=hashed_password)

    if await db.users.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}

@router.get("/only_auth")
async def only_auth(
        db: DBDep,
        request: Request,
        access_token: Annotated[str | None, Cookie()] = None,
):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Access token required or expired")

    return {
        "authorised": "Pass",
        "access_token": access_token
    }
