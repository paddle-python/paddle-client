import logging
from typing import List
from urllib.parse import urljoin

from .types import PaddleJsonType

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
    `List Users (subscription) Paddle docs <https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers>`_

    Note: response does not include any information in pages and totals
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/users')

    states = ['active', 'past due', 'trialling', 'paused', 'deleted']
    if state is not None and state not in states:
        raise ValueError('state must be one of {0}'.format(', '.join(states)))

    json = {
        'subscription_id': subscription_id,
        'plan_id': plan_id,
        'state': state,
        'page': page,
        'results_per_page': results_per_page,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)


def cancel_subscription(
    self,
    subscription_id: int,
) -> bool:
    """
    `Cancel Subscription Paddle docs <https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/users_cancel')
    return self.post(url=url, json={'subscription_id': subscription_id})


def update_subscription(
    self,
    subscription_id: int,
    quantity: int = None,
    currency: str = None,
    recurring_price: float = None,
    bill_immediately: bool = None,
    plan_id: int = None,
    prorate: bool = None,
    keep_modifiers: bool = None,
    passthrough: str = None,
    pause: bool = None
) -> dict:
    """
    `Update Subscription Paddle docs <https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/users/update')

    currency_codes = ['USD', 'GBP', 'EUR']
    if currency and currency not in currency_codes:
        raise ValueError('currency must be one of {0}'.format(', '.join(currency_codes)))  # NOQA: E501

    json = {
        'subscription_id': subscription_id,
        'quantity': quantity,
        'currency': currency,
        'recurring_price': recurring_price,
        'bill_immediately': bill_immediately,
        'plan_id': plan_id,
        'prorate': prorate,
        'keep_modifiers': keep_modifiers,
        'passthrough': passthrough,
        'pause': pause,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)


def pause_subscription(self, subscription_id: int) -> dict:
    """
    `Update Subscription Paddle docs <https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser>`_

    There is no Pause Subscription endpoint in Paddle's API. This is a
    convenient helper method for update_subscription as no extra data can be
    sent when pausing/resuming subscriptions
    """  # NOQA: E501
    return self.update_subscription(  # pragma: no cover
        subscription_id=subscription_id, pause=True
    )


def resume_subscription(self, subscription_id: int) -> dict:
    """
    `Update Subscription Paddle docs <https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser>`_

    There is no Resume Subscription endpoint in Paddle's API. This is a
    convenient helper method for update_subscription as no extra data can be
    sent when pausing/resuming subscriptions
    """  # NOQA: E501
    return self.update_subscription(  # pragma: no cover
        subscription_id=subscription_id, pause=False
    )
