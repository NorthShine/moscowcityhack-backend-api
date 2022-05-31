from fastapi import Request, APIRouter
from httpx import AsyncClient

from config import get_config

parser_router = APIRouter(
    prefix='/api/parser',
    tags=['parser'],
)
client = AsyncClient()
config = get_config()


@parser_router.post('/url')
async def url_parser(request: Request):
    url = (await request.json())['url']
    response = await client.get(config['NEWS_PARSER'] + url, timeout=10000)
    data = response.json()
    return {'title': data['title'], 'author': data['author']}


@parser_router.post('/text')
async def text_parser(request: Request):
    text = (await request.json())['text']
    return {}
