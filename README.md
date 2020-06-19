# Paddle Client

A python (3.5+) wrapper around the [Paddle.com](https://paddle.com/) [API](https://developer.paddle.com/api-reference/intro)

If you are looking at intergrating Paddle with Django check out [dj-paddle](https://github.com/paddle-python/dj-paddle)

_Note: This is a work in progress, not all of the Paddle endpoints have been implemented yet_

## Quick start

### Installation

```bash
pip install paddle-client
```


### Usage

To use the Paddle API you will need a Paddle Vendor ID and API key which can be found on [Paddle's authentication page](https://vendors.paddle.com/authentication)

```python
from paddle import PaddleClient


paddle = PaddleClient(vendor_id=12345, api_key='myapikey')
paddle.list_products()
```

If `vendor_id` and `api_key` are not passed through when initalising Paddle will fall back and try and use environmental variables called `PADDLE_VENDOR_ID` and `PADDLE_API_KEY`
```bash
export PADDLE_VENDOR_ID=12345
export PADDLE_API_KEY="myapikey"
```

```python
from paddle import PaddleClient


paddle = PaddleClient()
paddle.list_products()
```


## Documentation

Coming soon. Please see `Working endpoints` below for basic usage.


## Contributing

All contributions are welcome and appreciated. Please see [CONTRIBUTING.md](https://github.com/paddle-python/paddle-client/blob/master/CONTRIBUTING.md) for more details including details on how to run tests etc.


## Working endpoints
* [Get Order Details](https://developer.paddle.com/api-reference/checkout-api/order-information/getorder)
* [Get User History](https://checkout.paddle.com/api/2.0/user/history)
* [Get Prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)
* [List Coupons](https://developer.paddle.com/api-reference/product-api/coupons/listcoupons)
* [Create Coupon](https://developer.paddle.com/api-reference/product-api/coupons/createcoupon)
* [Delete Coupon](https://developer.paddle.com/api-reference/product-api/coupons/deletecoupon)
* [Update Coupon](https://developer.paddle.com/api-reference/product-api/coupons/updatecoupon)
* [List Products](https://developer.paddle.com/api-reference/product-api/products/getproducts)
* [List Transactions](https://developer.paddle.com/api-reference/product-api/transactions/listtransactions)
* [Refund Payment](https://developer.paddle.com/api-reference/product-api/payments/refundpayment)
* [List Plans](https://developer.paddle.com/api-reference/subscription-api/plans/listplans)
* [Create Plan](https://developer.paddle.com/api-reference/subscription-api/plans/createplan)
* [List Subscription Users](https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers)
* [Cancel Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser)
* [Update Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser)
* [Preview Subscription Update](https://developer.paddle.com/api-reference/subscription-api/subscription-users/previewupdate)
* [Get Webhook History](https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks)
* [Add Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/createmodifier)
* [Delete Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/deletemodifier)
* [List Modifiers](https://developer.paddle.com/api-reference/subscription-api/modifiers/listmodifiers)

```python
paddle.get_order_details(checkout_id=checkout_id)
paddle.get_user_history(email=email)
paddle.get_prices(product_ids=[product_id])
paddle.list_coupons(product_id=product_id)
paddle.create_coupon(
    coupon_type='product',
    discount_type='percentage',
    discount_amount=50,
    allowed_uses=1,
    recurring=False,
    currency='USD',
    product_ids=product_ids,
    coupon_code='50%OFF',
    description='50% off coupon over $10',
    expires=expires,
    minimum_threshold=10,
    group='paddle-python',
)
paddle.delete_coupon(coupon_code=new_coupon_code, product_id=product_id)
paddle.update_coupon(
    coupon_code=coupon_code,
    new_coupon_code='40%OFF',
    new_group='paddle-python-test',
    product_ids=[product_id],
    expires=expires,
    allowed_uses=1,
    currency='USD',
    minimum_threshold=10,
    discount_amount=40,
    recurring=True
)
paddle.list_products()
paddle.list_transactions(entity='subscription', entity_id=subscription_id)
paddle.refund_payment(order_id=order_id, amount=amount, reason=reason)
paddle.list_plans()
paddle.create_plan(
    plan_name='plan_name',
    plan_trial_days=14,
    plan_length=1,
    plan_type='month',
    main_currency_code='USD',
    initial_price_usd=50,
    recurring_price_usd=50,
)
paddle.list_subscription_users()
paddle.cancel_subscription(subscription_id=1234)
paddle.update_subscription(subscription_id=1234, pause=True)
paddle.preview_update_subscription(
    subscription_id=123,
    bill_immediately=True,
    quantity=101,
)
paddle.add_modifier(subscription_id=1234, modifier_amount=10.5)
paddle.delete_modifier(modifier_id=10)
paddle.list_modifiers()
paddle.get_webhook_history()
```


## Failing Endpoints

The below endpoints have been implimented but are not working correctly according to the tests. They have been commented out in `paddle/paddle.py` and the tests will skip is the methods do not exist

* [Generate License](https://developer.paddle.com/api-reference/product-api/licenses/createlicense) - `Paddle error 108 - Unable to find requested product`
* [Create pay link](https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink) -  `Paddle error 108 - Unable to find requested product`


## ToDo
* Fix generate license and create pay link endpoints
* Paddle API endpoints
    * [List Payments](https://developer.paddle.com/api-reference/subscription-api/payments/listpayments)
    * [Reschedule Payment](https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment)
    * [Create One-off Charge](https://developer.paddle.com/api-reference/subscription-api/one-off-charges/createcharge)
* Work out if we want to include 'alias' methods like pause_subscription
* Get test coverage to 100%
* Docs (auto docs?)
* Use `pytest-mock` `Spy` to check params, json, urls etc for test requests
    * Needed to any tests which skip due to missing data
* How to deal with the manual cleanup?
* Pull request template
* TravisCI?
* Dependabot
* Remove double call for exception error message checking - How to get the exception str from `pytest.raises()`? pytest-mock `Spy`?
* Add pytest warnings to provide direct links to Paddle for bits that need to be cleaned up
