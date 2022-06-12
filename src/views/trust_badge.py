"""
Trust badge views.
"""

from fastapi import Depends, Request, APIRouter
from fastapi_jwt_auth import AuthJWT

from config import get_config
from use_cases import get_whitelist_by_id

trust_badge_router = APIRouter(
    prefix='/api/trustbadge',
    tags=['trust_badge'],
)


@trust_badge_router.get('/')
async def get_trust_badge_by_id_view(id: int, request: Request):
    """Get trust badge by id."""
    whitelist_item = await get_whitelist_by_id(id)
    if whitelist_item.url in request.client.host:
        return {'is_trusted': True}
    return {'is_trusted': False}


@trust_badge_router.post('/')
async def set_trust_badge_by_id_view(request: Request, Authorize: AuthJWT = Depends()):
    """Set trust badge by id."""
    Authorize.jwt_required()
    item_id = (await request.json())['id']
    whitelist_item = await get_whitelist_by_id(item_id)
    origin = (get_config())['DOMAIN']
    if whitelist_item is not None:
        return {
            'script': f'<script async defer data-trustbadge-id=\"{item_id}\" '
                      f'src=\"{origin}/trust-badge/script.js\"></script>',
        }
    return {'error': 'URL is not found in whitelist'}
