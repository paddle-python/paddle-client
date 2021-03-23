import os

import pytest

from paddle import PaddleClient, PaddleException

from .fixtures import paddle_client  # NOQA: F401


class BadPaddleDataWarning(UserWarning):
    pass


@pytest.fixture()
def set_vendor_id(monkeypatch):
    monkeypatch.setenv('PADDLE_VENDOR_ID', '1234')


@pytest.fixture()
def set_api_key(monkeypatch):
    monkeypatch.setenv('PADDLE_API_KEY', 'abcdefghijklmnopqrstuvwxyz')


@pytest.fixture()
def set_sandbox(monkeypatch):
    monkeypatch.setenv('PADDLE_SANDBOX', 'true')


@pytest.fixture()
def set_vendor_id_to_invalid(monkeypatch):
    monkeypatch.setenv('PADDLE_VENDOR_ID', 'Not an int')


@pytest.fixture()
def unset_vendor_id(monkeypatch):
    monkeypatch.delenv('PADDLE_VENDOR_ID', raising=False)


@pytest.fixture()
def unset_api_key(monkeypatch):
    monkeypatch.delenv('PADDLE_API_KEY', raising=False)


def test_init_ignore_env_vars(set_vendor_id, set_api_key, set_sandbox):
    vendor_id = 9999
    api_key = 'not-env-var'
    sandbox = False
    client = PaddleClient(
        vendor_id=vendor_id,
        api_key=api_key,
        sandbox=sandbox,
    )
    assert client.vendor_id == vendor_id
    assert client.api_key == api_key
    assert client.sandbox == sandbox


def test_vendor_id_env_var(set_vendor_id):
    client = PaddleClient(api_key='test')
    assert client.vendor_id == int(os.environ['PADDLE_VENDOR_ID'])


def test_api_key_env_var(set_api_key):
    client = PaddleClient(vendor_id=1)
    assert client.api_key == os.environ['PADDLE_API_KEY']


def test_sandbox_env_var(set_sandbox):
    client = PaddleClient(vendor_id=1, api_key='test')
    assert client.sandbox is True


def test_sandbox_urls(paddle_client):  # NOQA: F811
    assert paddle_client.checkout_v1.startswith('https://sandbox-')
    assert paddle_client.checkout_v2.startswith('https://sandbox-')
    assert paddle_client.checkout_v2_1.startswith('https://sandbox-')
    assert paddle_client.vendors_v2.startswith('https://sandbox-')
    assert paddle_client.default_url == paddle_client.vendors_v2


def test_vendor_id_not_set(unset_vendor_id, unset_api_key):
    with pytest.raises(ValueError) as error:
        PaddleClient(api_key='test')
    error.match('Vendor ID not set')


def test_vendor_id_not_int(set_vendor_id_to_invalid):
    with pytest.raises(ValueError) as error:
        PaddleClient(api_key='test')
    error.match('Vendor ID must be a number')


def test_api_key_not_set(unset_vendor_id, unset_api_key):
    with pytest.raises(ValueError) as error:
        PaddleClient(vendor_id=1)
    error.match('API key not set')


def test_sandbox(paddle_client):  # NOQA: F811
    with pytest.raises(PaddleException) as error:
        paddle_client.post('https://sandbox-checkout.paddle.com/api/1.0/order')

    msg = 'HTTP error 405 - The method used for the Request is not allowed for the requested resource.'  # NOQA: E501
    error.match(msg)


def test_json_and_data(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.get(
            paddle_client.default_url,
            json={'a': 'b'},
            data={'a': 'b'}
        )
    error.match('Please set either data or json not both')


def test_bad_url(paddle_client):  # NOQA: F811
    with pytest.raises(PaddleException) as error:
        with pytest.warns(RuntimeWarning) as warning:
            paddle_client.get('/badurl')
    error.match('Paddle error 101 - Bad method call')

    warning_message = (
        'Paddle recieved a relative URL so it will attempt to join it to '
        'https://sandbox-vendors.paddle.com/api/2.0/ as it is the Paddle URL '
        'with the most endpoints. The full URL that will be used is: '
        'https://sandbox-vendors.paddle.com/api/2.0/badurl - You should '
        'specifiy the full URL as this default URL may change in the future.'
    )
    assert len(warning._list) == 1
    assert str(warning._list[0].message) == warning_message


def test_sandbox_warning(paddle_client):  # NOQA: F811
    with pytest.warns(RuntimeWarning) as warning:
        url = 'https://vendors.paddle.com/api/2.0/product/get_products'
        paddle_client.post(url)

    sandbox_url = 'https://sandbox-vendors.paddle.com/api/2.0/product/get_products'  # NOQA: E501
    warning_message = (
        'PaddleClient is configured in sandbox mode but the URL provided does '
        'not point to a sandbox subdomain. The URL will be converted to use '
        'the Paddle sandbox ({0})'.format(sandbox_url)
    )
    assert len(warning._list) == 1
    assert str(warning._list[0].message) == warning_message


def test_http_error(paddle_client):  # NOQA: F811
    with pytest.raises(PaddleException) as error:
        paddle_client.post('https://sandbox-checkout.paddle.com/api/1.0/order')

    message = 'HTTP error 405 - The method used for the Request is not allowed for the requested resource.'  # NOQA: E501
    error.match(message)
