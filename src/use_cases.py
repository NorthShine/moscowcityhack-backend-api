from db import users, whitelist, database


async def get_user_by_username(username):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


async def get_whitelist():
    query = whitelist.select()
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
