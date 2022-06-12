import typing

from sqlalchemy import func
from db import users, whitelist, database


async def get_user_by_username(username):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


async def get_whitelist(
        page: typing.Optional[int] = None,
        per_page: typing.Optional[int] = None,
):
    query = whitelist.select()
    if page is not None and per_page is not None:
        query = query.limit(per_page).offset(page)
    return await database.fetch_all(query)


async def add_url_to_whitelist(url):
    query = whitelist.insert().values(url=url)
    return await database.execute(query)


async def update_url_from_whitelist(url_id, new_url):
    query = whitelist.update().where(whitelist.c.id == url_id).values(url=new_url)
    await database.execute(query)


async def delete_url_from_whitelist(url_id):
    query = whitelist.delete().where(whitelist.c.id == url_id)
    await database.execute(query)


async def get_whitelist_by_id(whitelist_item_id):
    query = whitelist.select().where(whitelist.c.id == whitelist_item_id)
    return await database.fetch_one(query)
