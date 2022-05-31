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

    async def search(self, author, title, description, text):
        author_response = (await self.make_query(author))[0]
        title_response = (await self.make_query(title))[0]

        text = text or description
        nonuniqueness_hits = await self.check_nonuniqueness(text)

        parsed_data = {
            'nonuniqueness_hits': nonuniqueness_hits,
            'is_trusted_url': False,
            'is_real_author': False,
            'is_real_article': False,
            'article_url': None,
            'author': author,
            'title': title,
            'author_response': author_response,
            'title_response': title_response,
            'text': text,
        }
        if await self.is_trusted_url(author_response['url']) or await self.is_trusted_url(title_response['url']):
            parsed_data['is_trusted_url'] = True
        if (
            title in title_response['title'] or
            title_response['title'] in title or
            title in title_response['content']
        ):
            parsed_data['article_url'] = title_response['pretty_url']
            parsed_data['is_real_article'] = True
        if (
            author in author_response['title'] or
            author in author_response['url'] or
            author in author_response['content']
        ):
            parsed_data['is_real_author'] = True

        return parsed_data

    async def make_query(self, query):
        if query is None:
            return []
        response = await self.client.get(
            self.searx_url,
            params={
                'q': query,
                'format': 'json',
            },
        )
        return response.json()['results']

    async def is_trusted_url(self, url):
        whitelist_urls = await get_whitelist()
        for whitelist_url in whitelist_urls:
            if whitelist_url.url in url:
                return True
        return False

    async def check_nonuniqueness(self, text):
        hits = 0
        results = await self.make_query(text)
        for result in results:
            if text == result['title'] or text == result['content']:
                hits += 10
                continue
            if text in result['title'] or text in result['content']:
                hits += 1
        return hits
