import logging
from typing import List
from urllib.parse import urljoin

from .types import PaddleJsonType

log = logging.getLogger(__name__)


def add_modifier(
    self,
    subscription_id: int,
    modifier_amount: float,
    modifier_recurring: bool = True,
    modifier_description: str = '',
) -> dict:
    """
    `Add Modifier Paddle docs <https://developer.paddle.com/api-reference/subscription-api/modifiers/createmodifier>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/modifiers/create')

    json = {
        'subscription_id': subscription_id,
        'modifier_amount': modifier_amount,
        'modifier_recurring': modifier_recurring,
        'modifier_description': modifier_description,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)


def delete_modifier(self, modifier_id: int) -> dict:
    """
    `Delete Modifier Paddle docs <https://developer.paddle.com/api-reference/subscription-api/modifiers/deletemodifier>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/modifiers/delete')
    return self.post(url=url, json={'modifier_id': modifier_id})


def list_modifiers(
    self,
    subscription_id: int = None,
    plan_id: int = None
) -> List[dict]:
    """
    `List Modifiers Paddle docs <https://developer.paddle.com/api-reference/subscription-api/modifiers/listmodifiers>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/modifiers')

    json = {
        'subscription_id': subscription_id,
        'plan_id': plan_id,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)
