# Paddle Client

A python (3.5+) wrapper around the [Paddle.com API](https://developer.paddle.com/api-reference/intro)

If you are looking at integrating Paddle with Django check out [dj-paddle](https://github.com/paddle-python/dj-paddle)

The full documentation is available at: https://paddle-client.readthedocs.io

_Note: Several of the Paddle Endpoints are currently not working as expected. See [Failing endpoints](#failing-endpoints)_ below.

## Quick start

### Installation

```bash
pip install paddle-client
```


### Basic Usage

To use the Paddle API you will need a Paddle Vendor ID and API key which can be found on [Paddle's authentication page](https://vendors.paddle.com/authentication)

```python
from paddle import PaddleClient


paddle = PaddleClient(vendor_id=12345, api_key='myapikey')
paddle.list_products()
```

If `vendor_id` and `api_key` are not passed through when initialising Paddle will fall back and try and use environmental variables called `PADDLE_VENDOR_ID` and `PADDLE_API_KEY`
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

The full documentation is available on Read the Docs: https://paddle-client.readthedocs.io


## Contributing

All contributions are welcome and appreciated. Please see [CONTRIBUTING.md](https://github.com/paddle-python/paddle-client/blob/master/CONTRIBUTING.md) for more details including details on how to run tests etc.


## Paddle Endpoints

The below endpoints from the [Paddle API Reference](https://developer.paddle.com/api-reference) have been implemented

For full details see the [API Reference in the docs](https://paddle-client.readthedocs.io/en/latest/api_reference.html). This includes details on parameters and return types for all the different methods as well as other helper methods around the Paddle.com API.

See [`Usage`](#usage) below for quick examples.

**Checkout API**
* [Get Order Details](https://developer.paddle.com/api-reference/checkout-api/order-information/getorder)
* [Get User History](https://checkout.paddle.com/api/2.0/user/history)
* [Get Prices](https://developer.paddle.com/api-reference/checkout-api/prices/getprices)

**Product API**
* [List Coupons](https://developer.paddle.com/api-reference/product-api/coupons/listcoupons)
* [Create Coupon](https://developer.paddle.com/api-reference/product-api/coupons/createcoupon)
* [Delete Coupon](https://developer.paddle.com/api-reference/product-api/coupons/deletecoupon)
* [Update Coupon](https://developer.paddle.com/api-reference/product-api/coupons/updatecoupon)
* [List Products](https://developer.paddle.com/api-reference/product-api/products/getproducts)
* [List Transactions](https://developer.paddle.com/api-reference/product-api/transactions/listtransactions)
* [Refund Payment](https://developer.paddle.com/api-reference/product-api/payments/refundpayment)

**Subscription API**
* [List Plans](https://developer.paddle.com/api-reference/subscription-api/plans/listplans)
* [Create Plan](https://developer.paddle.com/api-reference/subscription-api/plans/createplan)
* [List Subscription Users](https://developer.paddle.com/api-reference/subscription-api/subscription-users/listusers)
* [Cancel Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/canceluser)
* [Update Subscription](https://developer.paddle.com/api-reference/subscription-api/subscription-users/updateuser)
* [Add Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/createmodifier)
* [Delete Modifier](https://developer.paddle.com/api-reference/subscription-api/modifiers/deletemodifier)
* [List Modifiers](https://developer.paddle.com/api-reference/subscription-api/modifiers/listmodifiers)
* [List Payments](https://developer.paddle.com/api-reference/subscription-api/payments/listpayments)
* [Reschedule Payment](https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment)
* [Create One-off Charge](https://developer.paddle.com/api-reference/subscription-api/one-off-charges/createcharge)

**Alert API**
* [Get Webhook History](https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks)


### Usage

See the [API Reference in the docs](https://paddle-client.readthedocs.io/en/latest/api_reference.html) for full usage with param are return details.

```python
# Checkout API
paddle.get_order_details(checkout_id='aaaa-bbbb-cccc-1234')
paddle.get_user_history(email='test@example.com')
paddle.get_prices(product_ids=[1234])

# Product API
paddle.list_coupons(product_id=1234)
paddle.create_coupon(
    coupon_type='product',
    discount_type='percentage',
    discount_amount=50,
    allowed_uses=1,
    recurring=False,
    currency='USD',
    product_ids=[1234],
    coupon_code='50%OFF',
    description='50% off coupon over $10',
    expires='2030-01-01 10:00:00',
    minimum_threshold=10,
    group='paddle-python',
)
paddle.delete_coupon(coupon_code='mycoupon', product_id=1234)
paddle.update_coupon(
    coupon_code='mycoupon',
    new_coupon_code='40%OFF',
    new_group='paddle-python-test',
    product_ids=[1234],
    expires='2030-01-01 10:00:00',
    allowed_uses=1,
    currency='USD',
    minimum_threshold=10,
    discount_amount=40,
    recurring=True
)
paddle.list_products()
paddle.list_transactions(entity='subscription', entity_id=1234)
paddle.refund_product_payment(order_id=1234, amount=0.01, reason='reason')

# Subscription API
paddle.list_plans()
paddle.get_plan(plan=123)
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
paddle.update_subscription(
    subscription_id=1234,
    quantity=10.00,
    currency='USD',
    recurring_price=10.00,
    bill_immediately=False,
    plan_id=123,
    prorate=True,
    keep_modifiers=True,
    passthrough='passthrough',
)
paddle.pause_subscription(subscription_id=1234)
paddle.resume_subscription(subscription_id=1234)
paddle.add_modifier(subscription_id=1234, modifier_amount=10.5)
paddle.delete_modifier(modifier_id=10)
paddle.list_modifiers()
paddle.list_subscription_payments()
paddle.reschedule_subscription_payment(payment_id=4567, date='2030-01-01')
paddle.create_one_off_charge(
    subscription_id=1234,
    amount=0.0,
    charge_name="Add X on top of subscription"
)

# Alert API
paddle.get_webhook_history()
```
