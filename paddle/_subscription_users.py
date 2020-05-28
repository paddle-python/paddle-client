import logging
from typing import List
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def list_subscription_users(
    self,
    subscription_id: int = None,
    plan_id: int = None,
    state: int = None,
    page: int = None,
    results_per_page: int = None,
) -> List[dict]:
    """
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers
    """
    url = urljoin(self.vendors_v2, 'subscription/users')

    states = ['active', 'past due', 'trialling', 'paused']
    if state is not None and state not in states:
        raise ValueError('state must be one of {0}'.format(', '.join(states)))

    json = {
        'subscription_id': subscription_id,
        'plan_id': plan_id,
        'state': state,
        'page': page,
        'results_per_page': results_per_page,
    }
    return self.post(url=url, json=json)


def cancel_subscription(
    self,
    subscription_id: int,
) -> bool:
    """
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser
    """
    url = urljoin(self.vendors_v2, 'subscription/users_cancel')
    return self.post(url=url, json={'subscription_id': subscription_id})
