
import asyncpg
import os

DB_CONFIG = {
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASS", "1234"),
    "database": os.getenv("PG_DB", "Panama"),
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
}



async def init_db():
    return await asyncpg.create_pool(
        min_size=1,
        max_size=10,
        **DB_CONFIG
    )
