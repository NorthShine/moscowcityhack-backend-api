from typing import List
from fastapi import HTTPException, Depends, Request

from fastapi_jwt_auth import AuthJWT

from src.app import app
from src.schemas import User, Whitelist
from src.use_cases import (
    add_url_to_whitelist,
    delete_url_from_whitelist,
    get_user_by_username,
    get_whitelist,
    update_url_from_whitelist,
)


@app.post('/api/admin/sign_in')
async def sign_in_view(user: User, Authorize: AuthJWT = Depends()):
    user_obj = await get_user_by_username(user.username)
    if not user_obj or user.password != user_obj.password:
        raise HTTPException(status_code=401, detail='No such user with these credentials')

    access_token = Authorize.create_access_token(subject=user.username)
    return {'access_token': access_token}


@app.get('/api/admin/whitelist', response_model=List[Whitelist])
async def get_whitelist_view():
    return await get_whitelist()


@app.post('/api/admin/whitelist', response_model=Whitelist)
async def add_url_to_whitelist_view(request: Request):
    data = await request.json()
    url_obj_id = await add_url_to_whitelist(data['url'])
    return {**data.dict(), 'id': url_obj_id}


@app.patch('/api/admin/whitelist/{url_id}', response_model=Whitelist)
async def update_url_in_whitelist_view(url_id: int, request: Request):
    data = await request.json()
    await update_url_from_whitelist(url_id, data['new_url'])
    return {**data.dict()}


@app.delete('/api/admin/whitelist/{url_id}')
async def delete_url_from_whitelist_view(url_id: int):
    await delete_url_from_whitelist(url_id)
    return {}
