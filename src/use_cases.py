import typing
from sqlalchemy import func
from sqlalchemy.sql import select

from db import users, whitelist, database, checked_urls


async def get_user_by_username(username):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


async def get_whitelist(
        page: typing.Optional[int] = None,
        per_page: typing.Optional[int] = None,
        q: typing.Optional[str] = None,
):
    query = whitelist.select()
    if q is not None:
        query = whitelist.select().filter(whitelist.c.url.ilike(f'%{q}%'))
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


async def append_url_to_checked(
        url,
        is_trusted_url,
        is_real_author,
        is_real_article):
    query = checked_urls.insert().values(
        url=url,
        is_real_article=is_real_article,
        is_real_author=is_real_author,
        is_trusted_url=is_trusted_url
    )
    return await database.execute(query)


async def count_checks_per_url():
    query = select(func.count(), checked_urls.c.url)\
        .group_by(checked_urls.c.url)
    return await database.fetch_all(query)
