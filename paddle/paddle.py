import logging
import os
import warnings
from urllib.parse import urljoin

import requests

log = logging.getLogger(__name__)


class PaddleException(Exception):

    def __init__(self, error):
        self.code = 'Unknown'
        self.message = str(error)
        if isinstance(error, requests.HTTPError):  # pragma: no cover - Unsure how to trigger a HTTPError here  # NOQA: E501
            self.code = int(error.response.status_code)
            self.message = f'HTTP error {self.code} - {error.response.content.decode("utf-8")}'  # NOQA
        elif isinstance(error, dict):
            try:
                self.code = int(error['code'])
                self.message = f'Paddle error {error["code"]} - {error["message"]}'  # NOQA
            except KeyError:  # pragma: no cover - Not sure if this is even possible  # NOQA: E501
                pass

    def __str__(self) -> str:
        return self.message


class Paddle():

    def __init__(self, vendor_id: int = None, api_key: str = None):
        if not vendor_id:
            try:
                vendor_id = int(os.environ['PADDLE_VENDOR_ID'])
            except KeyError:
                raise ValueError('Vendor ID not set')
            except ValueError:
                raise ValueError('Vendor ID must be a number')
        if not api_key:
            try:
                api_key = os.environ['PADDLE_API_KEY']
            except KeyError:
                raise ValueError('API key not set')

        self.checkout_v1 = 'https://checkout.paddle.com/api/1.0/'
        self.checkout_v2 = 'https://checkout.paddle.com/api/2.0/'
        self.checkout_v2_1 = 'https://vendors.paddle.com/api/2.1/'
        self.vendors_v2 = 'https://vendors.paddle.com/api/2.0/'
        self.default_url = self.vendors_v2

        self.vendor_id = vendor_id
        self.api_key = api_key
        self.json = {
            'vendor_id': self.vendor_id,
            'vendor_auth_code': self.api_key,
        }

        self.url_warning = (
            'Paddle recieved a relative URL so it will attempt to join it to '
            '{0} as it is the Paddle URL with the most endpoints. The full '
            'URL that will be used is: {1} - You should specifiy the full URL '
            'as this default URL may change in the future.'
        )

    def request(
        self,
        url: str,
        method: str = 'GET',
        params: dict = None,
        data: dict = None,
        json: dict = None
    ) -> dict:
        kwargs = {}  # type: dict

        # URL join will remove anything after the host name is the url
        # is prepended with a /
        if not url.startswith('http'):
            if url.startswith('/'):
                url = url[1:]
            url = urljoin(self.default_url, url)
            warning_message = self.url_warning.format(self.default_url, url)
            warnings.warn(warning_message, RuntimeWarning)
        if 'paddle.com/api/' not in url:
            raise ValueError('URL "{0}" does not appear to be a Paddle API URL')  # NOQA: E501
        kwargs['url'] = url

        kwargs['method'] = method.upper()

        if data and json:
            raise ValueError('Please set either data or json not both')
        if kwargs['method'] == 'GET' and (data or json):
            log.warn('GET data/json should not be provided with GET method.')

        if kwargs['method'] in ['POST', 'PUT', 'PATCH']:
            kwargs['json'] = {}
            if data:
                kwargs['json'] = data
            if json:
                kwargs['json'] = json
            kwargs['json'] = {k: v for k, v in kwargs['json'].items() if v is not None}  # NOQA: E501
            kwargs['json'].update(self.json)

        if params:
            kwargs['params'] = params

        response = requests.request(**kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:  # pragma: no cover - Unsure how to trigger a HTTPError here  # NOQA: E501
            raise PaddleException(e)

        response_json = response.json()  # type: dict

        if 'error' in response_json:
            raise PaddleException(response_json['error'])
        # API v1 does not include success
        if 'success' in response_json and not response_json['success']:  # pragma: no cover - Not sure if this is even possible  # NOQA: E501
            raise PaddleException(response_json)

        if 'response' in response_json and response_json['response'] is not None:  # NOQA: E501
            return response_json['response']

        if 'message' in response_json and response_json['message'] is not None:
            return response_json['message']

        # Response is only {"success": True}
        if len(response_json.keys()) == 1 and 'success' in response_json:
            return response_json['success']

        return response_json

    def get(self, url, **kwargs):
        kwargs['url'] = url
        kwargs['method'] = 'GET'
        return self.request(**kwargs)

    def post(self, url, **kwargs):
        kwargs['url'] = url
        kwargs['method'] = 'POST'
        return self.request(**kwargs)

    from ._order_information import get_order_details

    from ._user_history import get_user_history

    from ._prices import get_prices

    from ._coupons import list_coupons
    from ._coupons import create_coupon
    from ._coupons import delete_coupon
    from ._coupons import update_coupon

    from ._products import list_products

    # from ._licenses import generate_license

    # from ._pay_links import create_pay_link

    from ._transactions import list_transactions

    from ._payments import refund_payment

    from ._plans import list_plans
    # from ._plans import get_plan
    from ._plans import create_plan

    from ._subscription_users import list_subscription_users
    from ._subscription_users import cancel_subscription
    from ._subscription_users import update_subscription
    from ._subscription_users import preview_subscription_update
    # Alias to better match update_subscription
    from ._subscription_users import preview_subscription_update as preview_update_subscription  # NOQA: E501

    from ._webhooks import get_webhook_history
