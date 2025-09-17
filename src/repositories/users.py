from pydantic import EmailStr
from sqlalchemy import func, select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemes.users import User, UserRequestAdd, UserWithHashedPassword


class UsersRepository(BaseRepository):

    model = UsersOrm
    schema = User

    async def get_by_email(self, email: EmailStr) -> UserRequestAdd | None:
        q = select(self.model).where(func.lower(self.model.email) == email)
        res = await self.session.execute(q)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword:

        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()

        return UserWithHashedPassword.model_validate(model)