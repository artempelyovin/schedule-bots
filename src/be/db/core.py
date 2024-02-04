from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://schedule-api:123456@localhost:5432/schedule-api-db", echo=True
)  # TODO: хардкод + echo

Session = async_sessionmaker(engine)
