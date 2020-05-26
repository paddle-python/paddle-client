# Paddle Python

A python (3+) wrapper around the Paddle API

This is a work in progress, not all of the Paddle endpoints have been implimented yet

## Quick start

### Installation

This package is not yet on Pypi (as the name `paddle` name it taken and we can't think of anything better right now) so until then you can install it straight from Github:
```
pip install git+https://github.com/pyepye/paddle-python
```


### Usage

```python
from paddle import Paddle


paddle = Paddle(vendor_id=12345, api_key='myapikey')
paddle.list_products()
```

If `vendor_id` and `api_key` are not passed through when initalising Paddle will fall back and try and use environmental variables called `PADDLE_VENDOR_ID` and `PADDLE_API_KEY`
```bash
export PADDLE_VENDOR_ID=12345
export PADDLE_API_KEY="myfakeapikey"
```

```python
from paddle import Paddle


paddle = Paddle()
paddle.list_products()
```


## Working endpoints


* [Get Order Details](https://developer.paddle.com/api-reference/checkout-api/order-information/getorder)
* [Get User History](https://checkout.paddle.com/api/2.0/user/history)
* [Get Prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)
* [List Coupons](https://developer.paddle.com/api-reference/product-api/coupons/listcoupons)
* [Create Coupon](https://developer.paddle.com/api-reference/product-api/coupons/createcoupon)
* [Delete Coupon](https://developer.paddle.com/api-reference/product-api/coupons/deletecoupon)
* [Update Coupon](https://developer.paddle.com/api-reference/product-api/coupons/updatecoupon)
* [List Products](https://developer.paddle.com/api-reference/product-api/products/getproducts)
* [List Plans](https://developer.paddle.com/api-reference/subscription-api/plans/listplans)
* [Get Webhook History](https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks)

```python
paddle.get_order_details(checkout_id=checkout_id)
paddle.get_user_history(email=email)
paddle.get_prices(product_ids=[product_id])
paddle.list_coupons(product_id=product_id)
paddle.create_coupon(
    coupon_type=coupon_type,
    discount_type=discount_type,
    discount_amount=discount_amount,
    allowed_uses=allowed_uses,
    recurring=recurring,
    currency=currency,
    product_ids=product_ids,
    coupon_code=coupon_code,
    description=description,
    expires=expires,
    minimum_threshold=minimum_threshold,
    group=group,
)
paddle.delete_coupon(coupon_code=new_coupon_code, product_id=product_id)
paddle.update_coupon(
    coupon_code=coupon_code,
    new_coupon_code=new_coupon_code,
    new_group='paddle-python-test',
    product_ids=[product_id],
    expires=expires,
    allowed_uses=allowed_uses,
    currency=currency,
    minimum_threshold=9998,
    discount_amount=discount_amount,
    recurring=True
)
paddle.list_products()
paddle.list_plans()
paddle.get_webhook_history()
```


## Failing Endpoints

The below endpoints have been implimented but are not working correctly according to the tests. They have been commented out in `paddle/paddle.py` and the tests will skip is the methods do not exist

* [Generate License](https://developer.paddle.com/api-reference/product-api/licenses/createlicense) - `Paddle error 108 - Unable to find requested product`
* [Create pay link](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) -  `Paddle error 108 - Unable to find requested product`


## ToDo
* Fix generate license and create pay link endpoints
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
