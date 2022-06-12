"""
Statistics views.
"""

from fastapi import APIRouter

from use_cases import count_checks_per_url


statistics_router = APIRouter(
    prefix='/api/statistics',
    tags=['parser'],
)


@statistics_router.get('/checks_per_site')
async def get_checks_per_site():
    """Get stats per site."""
    urls = await count_checks_per_url()
    urls = [dict(count=c, url=url) for c, url in urls]
    return urls
