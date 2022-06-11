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

    async def search(self, author, title, description, text, url):
        author_response = await self.make_query(author)
        if author_response is not None:
            author_response = author_response[0]
        else:
            author_response = {"url": "No url found"}

        title_response = await self.make_query(title)
        if title_response is not None:
            title_response = title_response[0]
        else:
            title_response = {"url": "No url found"}

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

        is_author_url_trusted = await self.is_trusted_url(author_response['url'])
        is_title_url_trusted = await self.is_trusted_url(title_response['url'])
        is_url_trusted = await self.is_trusted_url(url) 
        if is_author_url_trusted or is_title_url_trusted or is_url_trusted:
            parsed_data['is_trusted_url'] = True

        author_title = author_response.get('title', '') + ' ' + \
                       author_response.get('url', '') + ' ' + \
                       author_response.get('content', '')
        
        if author in author_title:
            parsed_data['is_real_author'] = True
        
        are_titles_intersecting = title in title_response.get('title') or \
                                  title_response.get('title') in title
                 
        if are_titles_intersecting or title in title_response.get('content'):
            parsed_data['article_url'] = title_response['pretty_url']
            parsed_data['is_real_article'] = True

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
        return response.json().get('results')

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
