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
            author_responses = author_response[:5]
        else:
            author_responses = [{"url": "No url found"}]

        title_response = await self.make_query(title)
        if title_response is not None:
            title_responses = title_response[:5]
        else:
            title_responses = {"url": "No url found"}

        text = text or description
        nonuniqueness_hits = await self.check_nonuniqueness(text)

        parsed_data = {
            'nonuniqueness_hits': nonuniqueness_hits,
            'is_trusted_url': False,
            'is_real_author': False,
            'is_real_article': False,
            'found_authors': [],
            'found_titles': [],
            'found_articles': [],
            'author': author,
            'title': title,
            'author_responses': author_responses,
            'title_responses': title_responses,
            'text': text,
        }

        is_url_trusted = await self.is_trusted_url(url)
        if is_url_trusted:
            parsed_data['is_trusted_url'] = True

        await self.check_author_responses(author_responses, parsed_data, author)
        await self.check_title_responses(title_responses, parsed_data, title, url)

        return parsed_data

    async def check_author_responses(self, author_responses, parsed_data, author):
        for response in author_responses:
            if await self.is_trusted_url(response['url']):
                parsed_data['is_trusted_url'] = True
            author_title = response.get('title', '') + ' ' + \
                           response.get('url', '') + ' ' + \
                           response.get('content', '')
            if author in author_title:
                parsed_data['is_real_author'] = True
                parsed_data['found_authors'].append(author_title)

    async def check_title_responses(self, title_responses, parsed_data, title, url):
        for response in title_responses:
            if await self.is_trusted_url(response['url']):
                parsed_data['is_trusted_url'] = True
            are_titles_intersecting = title in response.get('title') or \
                                      response.get('title') in title

            are_urls_intersecting = url in response.get('url') or \
                                    url in response.get('pretty_url')

            if (
                    are_titles_intersecting or
                    are_urls_intersecting or
                    title in response.get('content')
            ):
                parsed_data['found_articles'].append(response['pretty_url'])
                parsed_data['found_titles'].append(response.get('title'))
                parsed_data['is_real_article'] = True

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
