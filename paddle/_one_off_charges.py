import logging
from urllib.parse import urljoin

from .types import PaddleJsonType

log = logging.getLogger(__name__)


def create_one_off_charge(
    self,
    subscription_id: int,
    amount: float,
    charge_name: str
) -> dict:
    """
    `Create One-off Charge Paddle docs <https://developer.paddle.com/api-reference/subscription-api/one-off-charges/createcharge>`_

    This endpoint currently only supports x-www-form-urlencoded not json
    unlike most of the other Paddle endpoints

    Note from Paddles API docs:

    Please put a proper product / charge name here to make it clear what buyers
    are buying. Here are some examples:

    - [add-on name] x [quantity] e.g. Supercool design plugin x 1

    - [number of credits] credits for [subscription plan] e.g. 200 credits for Monthly talk time

    - [quantity] [units] [product description] e.g. 124 MB data usage
    """  # NOQA: E501
    url = 'subscription/{0}/charge'.format(subscription_id)
    url = urljoin(self.vendors_v2, url)

    data = {
        'amount': amount,
        'charge_name': charge_name,
    }  # type: PaddleJsonType

    return self.post(url=url, data=data)
