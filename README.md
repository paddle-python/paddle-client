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

All tests are currently run against Paddle's API directly. No mocks are used as this is meant to be a thin wrapper. This does mean you need to set a few environmental variables specific to your Paddle account for the tests to run correctly.

```bash
poetry shell
vim .env
export PADDLE_TEST_DEFAULT_CHECKOUT_ID="..."
export PADDLE_TEST_DEFAULT_PRODUCT_ID=...
export PADDLE_TEST_DEFAULT_PLAN_ID=...
source .env
pytest tests/
# Coverage info is written to htmlcov/
```

### Cleanup

Parts of the Paddle API have create endpoints but not delete endpoints. Because of this several tests need to be cleaned up manually after they are run:


* `tests/test_licenses.py::test_generate_license`
* `tests/test_pay_links.py::test_create_pay_link`


## Working endpoints
* [Get Order Details](https://developer.paddle.com/api-reference/checkout-api/order-information/getorder)
* [Get User History](https://checkout.paddle.com/api/2.0/user/history)
* [Get Prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)
* [List Coupons](https://developer.paddle.com/api-reference/product-api/coupons/listcoupons)
* [Create Coupon](https://developer.paddle.com/api-reference/product-api/coupons/createcoupon)
* [Delete Coupon](https://developer.paddle.com/api-reference/product-api/coupons/deletecoupon)
* [Update Coupon](https://developer.paddle.com/api-reference/product-api/coupons/updatecoupon)
* [List products](https://developer.paddle.com/api-reference/product-api/products/getproducts)
* [List Plans](https://developer.paddle.com/api-reference/subscription-api/plans/listplans)
* [Get Webhook History](https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks)

## Failing Endpoints
* [Generate License](https://developer.paddle.com/api-reference/product-api/licenses/createlicense) - `Paddle error 108 - Unable to find requested product`
* [Create pay link](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) -  `Paddle error 108 - Unable to find requested product`


## ToDo
* Remove `base_url` from Paddle
* Paddle API endpoints
    * [List Transactions](https://developer.paddle.com/api-reference/product-api/transactions/listtransactions)
    * [Refund Payment](https://developer.paddle.com/api-reference/product-api/payments/refundpayment)
    * [Create Plan](https://developer.paddle.com/api-reference/subscription-api/plans/createplan)
    * [List Users](https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers)
    * [Cancel Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser)
    * [Update Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser)
    * [Preview Subscription Update](https://developer.paddle.com/api-reference/subscription-api/subscription-users/previewupdate)
    * [Add Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/createmodifier)
    * [Delete Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/deletemodifier)
    * [List Modifiers](https://developer.paddle.com/api-reference/subscription-api/modifiers/listmodifiers)
    * [List Payments](https://developer.paddle.com/api-reference/subscription-api/payments/listpayments)
    * [Reschedule Payment](https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment)
    * [Create One-off Charge](https://developer.paddle.com/api-reference/subscription-api/one-off-charges/createcharge)
* Work out the best way to deal with the different API urls
* tox setup
* Do we want to have a set of tests which use mocks?
    * Could use pytest-recording (vcrpy) to update Mock data
    * Github actions to recreate mocks nightly?
    * How to deal with different vendor_ids etc?
    * Mock httpx to check params, json, urls etc?
    * How to deal with the manual cleanup
* pytest-watch and pytest-testmon for faster TDD?
* Pull request template
* Travis?
    * Test results in pull request
    * Coverage info in pull request
* Release to pypi
* Dependabot
* Remove double call for exception error message checking. How to get the exception str from `pytest.raises()`
