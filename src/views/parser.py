from fastapi import Request

from src.app import app, client, config


@app.post('/api/parser/url')
async def url_parser(request: Request):
    url = (await request.json())['url']
    response = await client.get(config['NEWS_PARSER'] + url)
    return {}


@app.post('/api/parser/text')
async def text_parser(request: Request):
    text = (await request.json())['text']
    return {}
