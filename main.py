import asyncio
from engene import DatabaseSessionManager
from models.base import ModelBase
from models import init


async def create_tables():
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    async with session.engine.begin() as connection:
        await connection.run_sync(init.ModelBase.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
