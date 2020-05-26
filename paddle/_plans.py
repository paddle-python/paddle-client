import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def list_plans(self, plan: int = None) -> dict:
    """
    https://developer.paddle.com/api-reference/subscription-api/plans/listplans
    """
    url = urljoin(self.vendors_v2, 'subscription/plans')

    if plan:
        return self.post(url=url, json={'plan': plan})

    return self.post(url=url)
