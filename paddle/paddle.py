import logging
import os
from urllib.parse import urljoin

import httpx

log = logging.getLogger(__name__)


class PaddleException(Exception):

    def __init__(self, error):
        self.code: str = 'Unknown'
        self.message = error
        if isinstance(error, httpx.HTTPError):  # pragma: no cover - Unsure how to trigger a HTTPError here  # NOQA: E501
            self.code = 'HTTP error {0}'.format(error.response.status_code)
            self.message = error.response.content.decode("utf-8")
        elif isinstance(error, dict):
            try:
                self.code = 'Paddle error {0}'.format(error['code'])
                self.message = error['message']
            except KeyError:  # pragma: no cover - Not sure if this is even possible  # NOQA: E501
                pass

    def __str__(self) -> str:
        return '{0} - {1}'.format(self.code, self.message)


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

        self.base_url: str = 'https://vendors.paddle.com/api/2.0/'
        # url = 'https://checkout.paddle.com/api/1.0/order'
        # url = 'https://checkout.paddle.com/api/2.0/user/history'
        self.vendor_id: int = vendor_id
        self.api_key: str = api_key
        self.json: dict = {
            'vendor_id': self.vendor_id,
            'vendor_auth_code': self.api_key,
        }

    def request(
        self,
        url: str,
        method: str = 'GET',
        params: dict = None,
        data: dict = None,
        json: dict = None
    ) -> dict:
        kwargs: dict = {}

        # URL join will remove anything after the host name is the url
        # is prepended with a /
        if not url.startswith('http'):
            if url.startswith('/'):
                url = url[1:]
            url = urljoin(self.base_url, url)
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
            kwargs['json'].update(self.json)

        if params:
            kwargs['params'] = params

        response = httpx.request(**kwargs)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:  # pragma: no cover - Unsure how to trigger a HTTPError here  # NOQA: E501
            raise PaddleException(e)

        response_json: dict = response.json()
        if 'error' in response_json:
            raise PaddleException(response_json['error'])
        # API v1 does not include success
        if 'success' in response_json and not response_json['success']:  # pragma: no cover - Not sure if this is even possible  # NOQA: E501
            raise PaddleException(response_json)

        if 'response' in response_json:
            return response_json['response']
        return response_json

    def get(self, url, **kwargs):
        kwargs['url'] = url
        kwargs['method'] = 'GET'
        return self.request(**kwargs)

    def post(self, url, **kwargs):
        kwargs['url'] = url
        kwargs['method'] = 'POST'
        return self.request(**kwargs)

    def get_order_details(self, checkout_id: str, url: str = None) -> dict:
        # Accept URL for compatibility with a new API if it arrives
        if not url:
            url = 'https://checkout.paddle.com/api/1.0/order'
        params = {'checkout_id': checkout_id}
        return self.get(url=url, params=params)

    def get_user_history(self, email: str, vendor_id: int = None, product_id: int = None) -> dict:  # NOQA: E501
        url = 'https://checkout.paddle.com/api/2.0/user/history'

        params = {'email': email}
        if product_id:
            params['product_id'] = product_id

        if vendor_id:
            params['vendor_id'] = vendor_id
        else:
            params['vendor_id'] = self.vendor_id

        return self.get(url=url, params=params)
