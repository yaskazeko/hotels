from pydantic import EmailStr
from sqlalchemy import select, func

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemes.users import User, UserRequestAdd


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