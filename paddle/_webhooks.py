import logging
from urllib.parse import urljoin

from .validators import validate_datetime

log = logging.getLogger(__name__)


def get_webhook_history(
    self,
    page: int = None,
    alerts_per_page: int = None,
    query_head=None,
    query_tail=None,
) -> dict:
    url = urljoin(self.vendors_v2, 'alert/webhooks')

    json = {
        'page': page,
        'alerts_per_page': alerts_per_page,
    }
    if query_head:
        json['query_head'] = validate_datetime(query_head, 'query_head')
    if query_tail:
        json['query_tail'] = validate_datetime(query_tail, 'query_tail')

    return self.post(url=url, json=json)
