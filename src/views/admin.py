import math
from typing import Optional

from fastapi import HTTPException, Depends, Request, APIRouter

from fastapi_jwt_auth import AuthJWT

from schemas import User, Whitelist
from use_cases import (
    add_url_to_whitelist,
    delete_url_from_whitelist,
    get_user_by_username,
    get_whitelist,
    update_url_from_whitelist,
)

admin_router = APIRouter(
    prefix='/api/admin',
    tags=['admin'],
)


@admin_router.post('/sign_in')
async def sign_in_view(user: User, Authorize: AuthJWT = Depends()):
    user_obj = await get_user_by_username(user.username)
    if not user_obj or user.password != user_obj.password:
        raise HTTPException(status_code=401, detail='No such user with these credentials')

    access_token = Authorize.create_access_token(subject=user.username)
    return {'access_token': access_token}


@admin_router.get('/whitelist')
async def get_whitelist_view(
        q: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 5,
        Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    whitelist_count = len(await get_whitelist(q=q))
    whitelist_items = await get_whitelist(page, per_page, q)
    return {
        'data': whitelist_items,
        'page': page,
        'per_page': per_page,
        'last_page': math.ceil(whitelist_count / per_page),
    }


@admin_router.post('/whitelist', response_model=Whitelist)
async def add_url_to_whitelist_view(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    data = await request.json()
    url_obj_id = await add_url_to_whitelist(data['url'])
    return {**data, 'id': url_obj_id}


@admin_router.patch('/whitelist/{url_id}', response_model=Whitelist)
async def update_url_in_whitelist_view(url_id: int, request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    data = await request.json()
    await update_url_from_whitelist(url_id, data['new_url'])
    return {'id': url_id, 'url': data['new_url']}


@admin_router.delete('/whitelist/{url_id}')
async def delete_url_from_whitelist_view(url_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    await delete_url_from_whitelist(url_id)
    return {}
