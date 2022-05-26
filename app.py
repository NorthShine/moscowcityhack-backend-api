from fastapi import FastAPI, Request
from httpx import AsyncClient

from config import NEWS_PARSER

app = FastAPI()
client = AsyncClient()


@app.post('/api/parser/url')
async def url_parser(request: Request):
    url = (await request.json())['url']
    response = await client.get(NEWS_PARSER + url)
    return {}


@app.post('/api/parser/text')
async def text_parser(request: Request):
    text = (await request.json())['text']
    return {}
