Getting started
===============

Paddle Client is a python (3.5+) wrapper around the `Paddle.com API <https://developer.paddle.com/api-reference/intro>`_


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
