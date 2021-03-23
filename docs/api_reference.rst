API Reference
=============

Below is a :ref:`full list<Full reference>` of the Paddle Client methods. :ref:`Supported Paddle endpoints` lists the Paddle API endpoints in the same order as they are in the `Paddle API Reference <https://developer.paddle.com/api-reference>`_

There are also several *helper* methods implimented on top of the Paddle endpoints to make usage of the API easier.

For example the ``pause_subscription`` and ``resume_subscription`` methods have been added on top of ``update_subscription`` as to pause or resume a subscription the ``update_subscription`` endpoint is used but only the ``pause`` parameter can be set (and will fail if any others are).


Supported Paddle endpoints
--------------------------

As listed in the `Paddle API Reference <https://developer.paddle.com/api-reference>`_

**Checkout API**

- :meth:`Get Order Details<paddle.PaddleClient.get_order_details>`
- :meth:`Get User History<paddle.PaddleClient.get_user_history>`
- :meth:`Get Prices<paddle.PaddleClient.get_prices>`

**Product API**

- :meth:`List Coupons<paddle.PaddleClient.list_coupons>`
- :meth:`Create Coupon<paddle.PaddleClient.create_coupon>`
- :meth:`Delete Coupon<paddle.PaddleClient.delete_coupon>`
- :meth:`Update Coupon<paddle.PaddleClient.update_coupon>`
- :meth:`List Products<paddle.PaddleClient.list_products>`
- :meth:`List Transactions<paddle.PaddleClient.list_transactions>`
- :meth:`Refund Payment<paddle.PaddleClient.refund_product_payment>`

**Subscription API**

- :meth:`List Plans<paddle.PaddleClient.list_plans>` - (Including :meth:`Get Plan<paddle.PaddleClient.get_plan>`)
- :meth:`Create Plan<paddle.PaddleClient.create_plan>`
- :meth:`List Subscription Users<paddle.PaddleClient.list_subscription_users>`
- :meth:`Cancel Subscription<paddle.PaddleClient.cancel_subscription>`
- :meth:`Update Subscription<paddle.PaddleClient.update_subscription>` - (Including :meth:`Pause Subscription<paddle.PaddleClient.pause_subscription>` and :meth:`Resume Subscription<paddle.PaddleClient.resume_subscription>`)
- :meth:`Add Modifier<paddle.PaddleClient.add_modifier>`
- :meth:`Delete Modifier<paddle.PaddleClient.delete_modifier>`
- :meth:`List Modifiers<paddle.PaddleClient.list_modifiers>`
- :meth:`List Payments<paddle.PaddleClient.list_subscription_payments>`
- :meth:`Reschedule Payment<paddle.PaddleClient.reschedule_subscription_payment>`
- :meth:`Create One-off Charge<paddle.PaddleClient.create_one_off_charge>`

**Alert API**

- :meth:`Get Webhook History<paddle.PaddleClient.get_webhook_history>`



Broken endpoints
----------------

The below endpoints have been implimented but are not working correctly according to the tests. They have been commented out in ``paddle/paddle.py`` and the tests will skip is the methods do not exist

- `Generate License  <https://developer.paddle.com/api-reference/product-api/licenses/createlicense>`_ - ``Paddle error 108 - Unable to find requested product``
- `Create pay link  <https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink>`_ - ``Paddle error 108 - Unable to find requested product``
- `Reschedule subscription payment  <https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment>`_ - ``Paddle error 122 - Provided date is not valid``


Full reference
--------------

For reference on how to use. An example on how to use :meth:`List Products<paddle.PaddleClient.list_products>`:

.. code-block:: python

    from paddle import PaddleClient

    paddle = PaddleClient(vendor_id=12345, api_key='myapikey')
    paddle.list_products()



.. autoclass:: paddle.PaddleClient
   :members:
