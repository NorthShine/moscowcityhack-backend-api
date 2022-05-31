from use_cases import get_whitelist


class SearxManager:
    def __init__(
        self,
        config: dict,
        client,
    ):
        self.config = config
        self.client = client
        self.searx_url = config['SEARX_URL']

    async def search(self, author, title):
        author_response = await self.make_query(author)
        title_response = await self.make_query(title)

        parsed_data = {
            'is_trusted_url': False,
            'is_real_author': False,
            'is_real_article': False,
            'article_url': None,
            'author': author,
            'title': title,
            'author_response': author_response,
            'title_response': title_response,
        }
        if await self.is_trusted_url(author_response['url']) or await self.is_trusted_url(title_response['url']):
            parsed_data['is_trusted_url'] = True
        if title in title_response['title'] or title_response['title'] in title:
            parsed_data['article_url'] = title_response['pretty_url']
            parsed_data['is_real_article'] = True
        if author in author_response['title'] or author in author_response['url']:
            parsed_data['is_real_author'] = True

        return parsed_data

    async def make_query(self, query):
        response = await self.client.get(
            self.searx_url,
            params={
                'q': query,
                'format': 'json',
            },
        )
        return response.json()['results'][0]

    async def is_trusted_url(self, url):
        whitelist_urls = await get_whitelist()
        for whitelist_url in whitelist_urls:
            if whitelist_url.url in url:
                return True
        return False
