"""
Parser views.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient

from pydantic import BaseModel
from config import get_config
from searx_manager import SearxManager

from use_cases import append_url_to_checked

parser_router = APIRouter(
    prefix='/api/parser',
    tags=['parser'],
)
client = AsyncClient()
config = get_config()
searx = SearxManager(config, client)


class TextItem(BaseModel):
    text: str
    author: Optional[str] = None
    title: Optional[str] = None


class URLItem(BaseModel):
    url: str


@parser_router.post('/url')
async def url_parser(item: URLItem):
    """URL parser view."""
    url = item.url
    response = await client.get(config['NEWS_PARSER'] + url, timeout=10000)
    data = response.json()
    try:
        data = await searx.search(
            data['text'],
            data['author'],
            data['title'],
            data['description'],
            url,
            data.get('isArticle', False),
        )
    except Exception as e:
        reason = {'error': str(e)}
        raise HTTPException(status_code=400, detail=reason)

    is_trusted_url = data.get('is_trusted_url', False)
    is_real_author = data.get('is_real_author', False)
    is_real_article = data.get('is_real_article', False)
    truth_percentage = data.get('truth_percentage', 0)
    uniqueness_hits = data.get('uniqueness_hits', 0)

    await append_url_to_checked(
        url,
        is_trusted_url,
        is_real_author,
        is_real_article,
        truth_percentage,
        uniqueness_hits)

    return {'data': data}


@parser_router.post('/text')
async def text_parser(text_item: TextItem):
    """Text parser view."""
    text = text_item.text
    author = text_item.author
    title = text_item.title

    try:
        data = await searx.search(
            text,
            author,
            title,
        )
    except Exception as e:
        reason = {'error': str(e)}
        raise HTTPException(status_code=400, detail=reason)
    return {'data': data}
