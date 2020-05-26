import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def list_plans(self, plan: int = None) -> dict:
    url = urljoin(self.vendors_v2, 'subscription/plans')

    if plan:
        return self.post(url=url, json={'plan': plan})

    return self.post(url=url)
