from fastapi import Request, APIRouter

from use_cases import get_whitelist_by_id

trust_badge_router = APIRouter(
    prefix='/api/trustbadge',
    tags=['trust_badge'],
)


@trust_badge_router.get('/')
async def get_trust_badge_by_id_view(id: int, request: Request):
    whitelist_item = await get_whitelist_by_id(id)
    if whitelist_item.url in request.client.host:
        return {'is_trusted': True}
    return {'is_trusted': False}


@trust_badge_router.post('/')
async def set_trust_badge_by_id_view(request: Request):
    item_id = (await request.json())['id']
    whitelist_item = await get_whitelist_by_id(item_id)
    if whitelist_item is not None:
        return {
            'script': f'<script async defer data-trustbadge-id=\"{item_id}\" '
                      f'src=\”{request.client.host}/trustbadge/script.js\”></script>',
        }
    return {'error': 'URL is not found in whitelist'}
