import pytest

from paddle import PaddleClient, PaddleException


class BadPaddleDataWarning(UserWarning):
    pass


@pytest.fixture(scope='session')
def paddle_client():
    paddle = PaddleClient()
    return paddle


@pytest.fixture()
def unset_vendor_id(monkeypatch):
    monkeypatch.delenv('PADDLE_VENDOR_ID', raising=False)


@pytest.fixture()
def set_vendor_id_to_invalid(monkeypatch):
    monkeypatch.setenv('PADDLE_VENDOR_ID', 'Not an int')


@pytest.fixture()
def unset_api_key(monkeypatch):
    monkeypatch.delenv('PADDLE_API_KEY', raising=False)


def test_paddle__manual_vendor_id_and_api_key(unset_vendor_id, unset_api_key):
    with pytest.raises(ValueError):
        PaddleClient(api_key='test')
    try:
        PaddleClient(api_key='test')
    except ValueError as error:
        assert str(error) == 'Vendor ID not set'


def test_paddle_vendor_id_not_set(unset_vendor_id):
    with pytest.raises(ValueError):
        PaddleClient(api_key='test')
    try:
        PaddleClient(api_key='test')
    except ValueError as error:
        assert str(error) == 'Vendor ID not set'


def test_paddle_vendor_id_not_int(set_vendor_id_to_invalid):
    with pytest.raises(ValueError) as error:
        PaddleClient(api_key='test')
    error.match('Vendor ID must be a number')


def test_paddle_api_key_not_set(unset_vendor_id, unset_api_key):
    with pytest.raises(ValueError) as error:
        PaddleClient(vendor_id=1)
    error.match('API key not set')


def test_sandbox(paddle_client):
    with pytest.raises(PaddleException) as error:
        paddle_client.post('https://sandbox-checkout.paddle.com/api/1.0/order')

    msg = 'HTTP error 405 - The method used for the Request is not allowed for the requested resource.'  # NOQA: E501
    error.match(msg)


def test_paddle_json_and_data(paddle_client):
    with pytest.raises(ValueError) as error:
        paddle_client.get('anyurl', json={'a': 'b'}, data={'a': 'b'})
    error.match('Please set either data or json not both')


def test_paddle_data_and_json(paddle_client):
    with pytest.raises(PaddleException) as error:
        paddle_client.get('/badurl')
    error.match('Paddle error 101 - Bad method call')


def test_paddle_http_error(paddle_client):
    with pytest.raises(PaddleException) as error:
        paddle_client.post('https://sandbox-checkout.paddle.com/api/1.0/order')

    message = 'HTTP error 405 - The method used for the Request is not allowed for the requested resource.'  # NOQA: E501
    error.match(message)
