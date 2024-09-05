import json
from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

engine = AsyncEngine(
    create_engine(
        "postgresql+asyncpg://bot:123456@localhost:5432/schedule",
        json_serializer=partial(json.dumps, ensure_ascii=False),  # для поддержки русских символов в JSON типах Postgres
        echo=True,
    )
)
Session = async_sessionmaker(engine)
