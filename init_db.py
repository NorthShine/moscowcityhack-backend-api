from src.config import get_config
from src.db import database, users


async def init_db():
    config = get_config()
    query = users.insert().values(
        username=config['ADMIN_USERNAME'],
        password=config['ADMIN_PASSWORD'],
    )
    await database.execute(query)
