
from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import CurrentUserDep, DBDep
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return {"message": "Successfully logged out"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(username=data.username, email=data.email, hashed_password=hashed_password)

    if await db.users.get_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    await db.users.add(new_user_data)
    await db.commit()
    return {"message": "User registered successfully"}


@router.get("/me")
async def get_current_user(
    current_user_id: CurrentUserDep,
    db: DBDep,
):
    user = await db.users.get_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
