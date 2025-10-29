
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None
    schema:BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all_hotels(self, *args, **kwargs):
         query = select(self.model)
         result = await self.session.execute(query)
         return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered(self, *filters, **filter_by):
        query = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]



    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def get_by_id(self, id: int):
        return await self.get_one_or_none(id=id)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

