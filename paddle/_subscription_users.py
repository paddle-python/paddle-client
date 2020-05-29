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
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers

    Note: response does not include any information in pages and totals
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
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)


# def list_subscriptions(self, **kwargs: dict) -> List[dict]:
#     """
#     https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers

#     This is a convenient alias for list_subscription_users as while the
#     other name matches the API name, it's not particularly guessable
#     """
#     return self.list_subscription_users(**kwargs)


# def get_subscription(self, subscription_id: int) -> dict:
#     """
#     https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers

#     There is no get_subscription endpoint in Paddle's API, This is a
#     convenient alias
#     """
#     for subscription in self.list_subscription_users():
#         if subscription['subscription_id'] == subscription_id:
#             return subscription
#     error = 'Unable to find subscription with id {0}'.format(subscription_id)
#     raise ValueError(error)


def cancel_subscription(
    self,
    subscription_id: int,
) -> bool:
    """
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser
    """
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
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser
    """
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


# def pause_subscription(self, subscription_id: int) -> dict:
#     """
#     https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser

#     There is no resume_subscription endpoint in Paddle's API. This is a
#     convenient alias for update_subscription as no extra data can be sent
#     when pausing/resuming subscriptions
#     """
#     return self.update_subscription(subscription_id=subscription_id, pause=True)  # NOQA: E501


# def resume_subscription(self, subscription_id: int) -> dict:
#     """
#     https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser

#     There is no resume_subscription endpoint in Paddle's API. This is a
#     convenient alias for update_subscription as no extra data can be sent
#     when pausing/resuming subscriptions
#     """
#     return self.update_subscription(subscription_id=subscription_id, pause=False)  # NOQA: E501


def preview_subscription_update(
    self,
    subscription_id: int,
    quantity: int = None,
    bill_immediately: bool = None,
    prorate: bool = None,
    plan_id: int = None,
    currency: str = None,
    recurring_price: float = None,
    keep_modifiers: bool = None,
) -> dict:
    """
    https://developer.paddle.com/api-reference/subscription-api/subscription-users/previewupdate
    """
    url = urljoin(self.vendors_v2, 'subscription/preview_update')

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
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)
