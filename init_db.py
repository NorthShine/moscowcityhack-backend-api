"""
Setup database with default login and password for admin account.
"""

import asyncio

from src.config import get_config
from src.db import database, users


async def init_db():
    """Init DB with default admin credentials."""
    config = get_config()
    query = users.insert().values(
        username=config['ADMIN_USERNAME'],
        password=config['ADMIN_PASSWORD'],
    )
    await database.execute(query)


if __name__ == '__main__':
    asyncio.run(init_db())
