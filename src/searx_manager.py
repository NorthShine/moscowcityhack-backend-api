"""
SearX manager. Contains all methods for processing and parsing the found data about news.
searx is required (https://searx.github.io/searx/).
"""

from text_analysis.compare_texts import comp_cosine_similarity
from use_cases import get_whitelist


class SearxManager:
    """SearX manager.

    :param: config - dictionary with project configuration
    :param: client - AsyncClient instance for making requests
    """
    def __init__(
            self,
            config: dict,
            client,
    ):
        """Initialization."""
        self.config = config
        self.client = client
        self.searx_url = config['SEARX_URL']

    async def search(
            self,
            text,
            author=None,
            title=None,
            description=None,
            url=None,
            is_article=False,
    ):
        """Search author, title and text by using searx. Process found info."""
        author_responses = []
        title_responses = []
        if author is not None:
            author_response = await self.make_query(author)
            if author_response is not None:
                author_responses = author_response[:5]

        if title is not None:
            title_response = await self.make_query(title)
            if title_response is not None:
                title_responses = title_response[:5]

        text = text or description
        uniqueness_hits = []
        for attribute in (title, text):
            uniqueness_hits.append(await self.check_uniqueness(attribute))

        parsed_data = {
            'truth_percentage': 0,
            'uniqueness_hits': min(uniqueness_hits),
            # 'alternative_title': get_summary(text),
            'is_trusted_url': False,
            'is_real_author': False,
            'is_real_article': False,
            'author': author,
            'title': title,
            'found_articles': [],
            'url': url,
            'is_article': is_article,
            'text': text,
            'found_authors': [],
            'found_titles': [],
            'found_content': [],
        }

        if url is not None:
            is_url_trusted = await self.is_trusted_url(url)
            if is_url_trusted:
                parsed_data['is_trusted_url'] = True

        await self.check_author_responses(author_responses, parsed_data, author)
        await self.check_title_responses(title_responses, parsed_data, title, url)
        await self.check_text_responses(text, parsed_data)

        return parsed_data

    async def check_author_responses(self, author_responses, parsed_data, author):
        """Parse searx responses and get information about author."""
        for response in author_responses:
            if await self.is_trusted_url(response['url']):
                parsed_data['is_trusted_url'] = True
            author_title = response.get('title', '') + ' ' + \
                           response.get('url', '') + ' ' + \
                           response.get('content', '')
            parsed_data['found_authors'].append(response)
            if author in author_title:
                parsed_data['is_real_author'] = True

    async def check_title_responses(self, title_responses, parsed_data, title, url=None):
        """Parse searx responses and get information about title."""
        for response in title_responses:
            if await self.is_trusted_url(response['url']):
                parsed_data['is_trusted_url'] = True
            are_titles_intersecting = title in response.get('title') or \
                                      response.get('title') in title

            if url is not None:
                url_hit = url in response.get('url')
            else:
                url_hit = False

            title_hits = comp_cosine_similarity(title, response.get('content'))

            if are_titles_intersecting or \
                    url_hit or \
                    title in response.get('content') or \
                    title_hits:
                parsed_data['found_articles'].append(response['url'])
                parsed_data['is_real_article'] = True
                parsed_data['is_real_author'] = True

    async def check_text_responses(self, text, parsed_data):
        """Parse searx responses and get information about text."""
        if len(text) > 170:
            text = text[:170]
        text_responses = (await self.make_query(text))[:5]
        for response in text_responses:
            title_hits = comp_cosine_similarity(text, response.get('title'))
            content_hits = comp_cosine_similarity(text, response.get('content'))
            parsed_data['found_content'].append(response)
            if title_hits > 0.9 or content_hits > 0.9:
                parsed_data['found_articles'].append(response['url'])
                parsed_data['is_real_article'] = True
                parsed_data['truth_percentage'] = int(float(max((title_hits, content_hits))) * 100)

    async def make_query(self, query):
        """Make searx query. Return found results."""
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
        """Check if the url is whitelisted."""
        whitelist_urls = await get_whitelist()
        for whitelist_url in whitelist_urls:
            if whitelist_url.url in url:
                return True
        return False

    async def check_uniqueness(self, text):
        """Analyze text uniqueness based on searx responses.
        100 hits means that is unique text, 0 hits - is non-unique text."""
        hits = 100
        results = await self.make_query(text)

        for result in results:
            title_hits = comp_cosine_similarity(text, result.get('title'))
            content_hits = comp_cosine_similarity(text, result.get('content'))
            if title_hits > 0.9 or content_hits > 0.9:
                hits -= 10
            if hits <= 0:
                break
        return hits
