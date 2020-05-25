# Paddle Python

A python (3+) wrapper around the Paddle API

This is a work in progress


## Setup
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
poetry install

vim .env
export PADDLE_VENDOR_ID=...
export PADDLE_API_KEY="..."

poetry shell
source .env
```

## Running tests
```bash
poetry shell
vim .env
export PADDLE_TEST_DEFAULT_CHECKOUT_ID="..."
export PADDLE_TEST_DEFAULT_PRODUCT_ID=...

source .env
pytest tests/
# Coverage info is written to htmlcov/
```


## Working endpoints
* [Get Order Details](https://developer.paddle.com/api-reference/checkout-api/order-information/getorder)
* [Get User History](https://checkout.paddle.com/api/2.0/user/history)


## ToDo
* Paddle API endpoints
    * https://developer.paddle.com/api-reference/checkout-api/prices/getprices
    * https://developer.paddle.com/api-reference/product-api/coupons/listcoupons
    * https://developer.paddle.com/api-reference/product-api/coupons/createcoupon
    * https://developer.paddle.com/api-reference/product-api/coupons/deletecoupon
    * https://developer.paddle.com/api-reference/product-api/coupons/updatecoupon
    * https://developer.paddle.com/api-reference/product-api/products/getproducts
    * https://developer.paddle.com/api-reference/product-api/licenses/createlicense
    * https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink
    * https://developer.paddle.com/api-reference/product-api/transactions/listtransactions
    * https://developer.paddle.com/api-reference/product-api/payments/refundpayment
    * https://developer.paddle.com/api-reference/subscription-api/plans/listplans
    * https://developer.paddle.com/api-reference/subscription-api/plans/createplan
    * https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers
    * https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser
    * https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser
    * https://developer.paddle.com/api-reference/subscription-api/subscription-users/previewupdate
    * https://developer.paddle.com/api-reference/subscription-api/modifiers/createmodifier
    * https://developer.paddle.com/api-reference/subscription-api/modifiers/deletemodifier
    * https://developer.paddle.com/api-reference/subscription-api/modifiers/listmodifiers
    * https://developer.paddle.com/api-reference/subscription-api/payments/listpayments
    * https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment
    * https://developer.paddle.com/api-reference/subscription-api/one-off-charges/createcharge
    * https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks
* Work out the best way to deal with the different API urls
* tox setup
* Mocks pytest-recording (vcrpy) for mocks?
    * How to deal with different vendor_ids etc?
    * Github actions to recreate mocks nightly?
* pytest-watch and pytest-testmon for faster TDD?
* Pull request template
* Travis?
    * Test results in pull request
    * Coverage info in pull request
* Release to pypi
* Dependabot
