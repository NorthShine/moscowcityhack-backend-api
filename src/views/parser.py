from fastapi import Request, APIRouter, HTTPException
from httpx import AsyncClient

from config import get_config
from searx_manager import SearxManager

parser_router = APIRouter(
    prefix='/api/parser',
    tags=['parser'],
)
client = AsyncClient()
config = get_config()
searx = SearxManager(config, client)


@parser_router.post('/url')
async def url_parser(request: Request):
    url = (await request.json())['url']
    response = await client.get(config['NEWS_PARSER'] + url, timeout=10000)
    data = response.json()
    try:
        data = await searx.search(
            data['text'],
            data['author'],
            data['title'],
            data['description'],
            url,
            data.get('isArticle', True),
        )
    except Exception as e:
        reason = {'error': str(e)}
        raise HTTPException(status_code=400, detail=reason)
    return {'data': data}


@parser_router.post('/text')
async def text_parser(request: Request):
    data = await request.json()
    text = data.get('text')
    author = data.get('author')
    title = data.get('title')

    if text is None:
        reason = {'data': {'error': 'text field is required'}}
        raise HTTPException(status_code=400, detail=reason) 

    try:
        data = await searx.search(
            text,
            author,
            title,
        )
    except Exception as e:
        data = {'error': str(e)}
    return {'data': data}
