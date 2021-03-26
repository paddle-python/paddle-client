import logging
import os
import warnings
from distutils.util import strtobool
from urllib.parse import urljoin

import requests

log = logging.getLogger(__name__)


class PaddleException(Exception):

    def __init__(self, error):
        self.code = 'Unknown'
        self.message = str(error)
        if isinstance(error, requests.HTTPError):  # pragma: no cover - Unsure how to trigger a HTTPError here  # NOQA: E501
            self.code = int(error.response.status_code)
            self.message = 'HTTP error {0} - {1}'.format(
                self.code,
                error.response.content.decode('utf-8'),
            )
        elif isinstance(error, dict):
            try:
                self.code = int(error['code'])
                self.message = 'Paddle error {0} - {1}'.format(
                    error['code'],
                    error['message'],
                )
            except KeyError:  # pragma: no cover - Not sure if this is even possible  # NOQA: E501
                pass

    def __str__(self) -> str:
        return self.message


class PaddleClient():
    """
    If ``vendor_id`` and ``api_key`` are not passed through when initalising
    Paddle will fall back and try and use environmental variables
    called ``PADDLE_VENDOR_ID`` and ``PADDLE_API_KEY``
    """

    def __init__(
        self,
        vendor_id: int = None,
        api_key: str = None,
        sandbox: bool = None,
    ):
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
        if sandbox is None:
            sandbox = bool(strtobool(os.getenv('PADDLE_SANDBOX', 'False')))

        self.sandbox = sandbox
        self.checkout_v1 = 'https://checkout.paddle.com/api/1.0/'
        self.checkout_v2 = 'https://checkout.paddle.com/api/2.0/'
        self.checkout_v2_1 = 'https://vendors.paddle.com/api/2.1/'
        self.vendors_v2 = 'https://vendors.paddle.com/api/2.0/'
        if self.sandbox:
            self.checkout_v1 = 'https://sandbox-checkout.paddle.com/api/1.0/'
            self.checkout_v2 = 'https://sandbox-checkout.paddle.com/api/2.0/'
            self.checkout_v2_1 = 'https://sandbox-vendors.paddle.com/api/2.1/'
            self.vendors_v2 = 'https://sandbox-vendors.paddle.com/api/2.0/'
        self.default_url = self.vendors_v2

        self.vendor_id = vendor_id
        self.api_key = api_key
        self.auth = {
            'vendor_id': self.vendor_id,
            'vendor_auth_code': self.api_key,
        }

        self.relative_url_warning = (
            'Paddle recieved a relative URL so it will attempt to join it to '
            '{0} as it is the Paddle URL with the most endpoints. The full '
            'URL that will be used is: {1} - You should specifiy the full URL '
            'as this default URL may change in the future.'
        )
        self.sandbox_url_warning = (
            'PaddleClient is configured in sandbox mode but the URL provided '
            'does not point to a sandbox subdomain. The URL will be converted '
            'to use the Paddle sandbox ({0})'
        )

    def request(
        self,
        url: str,
        method: str = 'GET',
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> dict:
        kwargs = {}  # type: dict

        # URL join will remove anything after the host name is the url
        # is prepended with a /
        if not url.startswith('http'):
            if url.startswith('/'):
                url = url[1:]
            url = urljoin(self.default_url, url)
            warning_message = self.relative_url_warning.format(self.default_url, url)  # NOQA: E501
            warnings.warn(warning_message, RuntimeWarning)
        elif 'paddle.com/api/' not in url:
            error = 'URL does not appear to be a Paddle API URL - {0}'
            raise ValueError(error.format(url))
        elif self.sandbox and '://sandbox-' not in url:
            url = url.replace('://', '://sandbox-', 1)
            warnings.warn(self.sandbox_url_warning.format(url), RuntimeWarning)

        kwargs['url'] = url

        kwargs['method'] = method.upper()

        if data and json:
            raise ValueError('Please set either data or json not both')
        if kwargs['method'] == 'GET' and (data or json):   # pragma: no cover
            log.warn('GET data/json should not be provided with GET method.')

        if kwargs['method'] in ['POST', 'PUT', 'PATCH']:
            if data:
                kwargs['data'] = data
                kwargs['data'] = {k: v for k, v in kwargs['data'].items() if v is not None}  # NOQA: E501
                kwargs['data'].update(self.auth)
            elif json:
                kwargs['json'] = json
                kwargs['json'] = {k: v for k, v in kwargs['json'].items() if v is not None}  # NOQA: E501
                kwargs['json'].update(self.auth)
            else:
                kwargs['json'] = self.auth

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

        # Response is {"response": None, "success": True}
        if 'response' in response_json and response_json['response'] is None:
            del response_json['response']
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

    from ._licenses import generate_license

    from ._pay_links import create_pay_link

    from ._transactions import list_transactions

    from ._product_payments import refund_product_payment

    from ._plans import list_plans
    from ._plans import get_plan
    from ._plans import create_plan

    from ._subscription_users import list_subscription_users
    from ._subscription_users import list_subscription_users as list_subscriptions  # NOQA: E501
    from ._subscription_users import cancel_subscription
    from ._subscription_users import update_subscription
    from ._subscription_users import pause_subscription
    from ._subscription_users import resume_subscription

    from ._modifiers import add_modifier
    from ._modifiers import delete_modifier
    from ._modifiers import list_modifiers

    from ._subscription_payments import list_subscription_payments
    from ._subscription_payments import reschedule_subscription_payment

    from ._one_off_charges import create_one_off_charge

    from ._webhooks import get_webhook_history
