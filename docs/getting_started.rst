Getting started
===============

Paddle Client is a python (3.6+) wrapper around the `Paddle.com API <https://developer.paddle.com/api-reference/intro>`_


Paddle authentication
---------------------

Before you get started you will need an account on `Paddle.com <https://paddle.com>`_ to generate authentication details.

Once you have an account go to the `Paddle authentication page <https://vendors.paddle.com/authentication>`_ and find out both your ``Vendor ID`` and ``API key``


Installation
------------

Install of the paddle client can be done via pip:

.. code-block:: bash

    pip install paddle-client



Usage
-----

.. code-block:: python

    from paddle import PaddleClient

    paddle = PaddleClient(vendor_id=12345, api_key='myapikey')
    paddle.list_products()


If ``vendor_id`` and ``api_key`` are not passed through when initalising Paddle will fall back and try and use environmental variables called ``PADDLE_VENDOR_ID`` and ``PADDLE_API_KEY``

.. code-block:: bash

    export PADDLE_VENDOR_ID=12345
    export PADDLE_API_KEY="myapikey"


.. code-block:: python

    from paddle import PaddleClient

    paddle = PaddleClient()
    paddle.list_products()


Paddle sandbox environment
--------------------------

The `Paddle sandbox environment <https://developer.paddle.com/getting-started/sandbox>`_ is a separate Paddle environment which can be used for development and testing. You are required to create a new account in this environment, different to your production account.

Once you have this account setup and configured you can user the sandbox account by passing ``sandbox=True`` when initialising the Paddle Client. This will send all API calls to the Paddle sandbox URLs instead of the production URLs


.. code-block:: python

    from paddle import PaddleClient

    paddle = PaddleClient(vendor_id=12345, api_key='myapikey', sandbox=True)


It is also possible to turn the sandbox environment on using an environmental variable called ``PADDLE_SANDBOX``:

.. code-block:: bash

    export PADDLE_SANDBOX="true"


.. code-block:: python

    from paddle import PaddleClient

    paddle = PaddleClient(vendor_id=12345, api_key='myapikey')
