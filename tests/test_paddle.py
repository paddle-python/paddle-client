import pytest

from paddle import Paddle, PaddleException, __version__


@pytest.fixture(scope='session')
def paddle_client():
    paddle = Paddle()
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


def test_version():
    assert __version__ == '0.1.0'


def test_paddle__manual_vendor_id_and_api_key(unset_vendor_id, unset_api_key):
    with pytest.raises(ValueError):
        Paddle(api_key='test')
    try:
        Paddle(api_key='test')
    except ValueError as error:
        assert str(error) == 'Vendor ID not set'


def test_paddle_vendor_id_not_set(unset_vendor_id):
    with pytest.raises(ValueError):
        Paddle(api_key='test')
    try:
        Paddle(api_key='test')
    except ValueError as error:
        assert str(error) == 'Vendor ID not set'


def test_paddle_vendor_id_not_int(set_vendor_id_to_invalid):
    with pytest.raises(ValueError):
        Paddle(api_key='test')
    try:
        Paddle(api_key='test')
    except ValueError as error:
        assert str(error) == 'Vendor ID must be a number'


def test_paddle_api_key_not_set(unset_api_key):
    with pytest.raises(ValueError):
        Paddle(vendor_id=1)
    try:
        Paddle(vendor_id=1)
    except ValueError as error:
        assert str(error) == 'API key not set'


def test_paddle_json_and_data(paddle_client):
    with pytest.raises(ValueError):
        paddle_client.get('anyurl', json={'a': 'b'}, data={'a': 'b'})
    try:
        paddle_client.get('anyurl', json={'a': 'b'}, data={'a': 'b'})
    except ValueError as error:
        assert str(error) == 'Please set either data or json not both'


def test_paddle_data_and_json(paddle_client):
    with pytest.raises(PaddleException):
        paddle_client.get('badurl')
    try:
        paddle_client.get('badurl')
    except PaddleException as error:
        assert str(error) == 'Paddle error 101 - Bad method call'


def test_paddle_http_error(paddle_client):
    with pytest.raises(PaddleException):
        paddle_client.post('https://checkout.paddle.com/api/1.0/order')
    try:
        paddle_client.post('https://checkout.paddle.com/api/1.0/order')
    except PaddleException as error:
        assert str(error) == 'HTTP error 405 - The method used for the Request is not allowed for the requested resource.'  # NOQA: E501
