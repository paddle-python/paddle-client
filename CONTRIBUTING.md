# How to contribute

Thanks for wanting to contribute to the Paddle python API wrapper. This wrapper is intended to be a 'thin' wrapper around the API and include no business logic.

Important Paddle resources:

  * [Paddle's Vendors Dashboard](https://vendors.paddle.com/overview) - Please make sure you have registered before you get started
  * [Paddle developer API reference](https://developer.paddle.com/api-reference/intro)


Python resources:

  * [Poetry](https://python-poetry.org/) for python packaging and dependency management
  * [Mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
  * [pytest](https://docs.pytest.org/en/latest/) for running test
  * [isort](https://timothycrosley.github.io/isort/) to keep all our imports looking nice and easy to follow
  * [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)


## Testing

This package uses the [Poetry](https://python-poetry.org/) for packaging and dependency management, before you get started please install it.

You will then need:
* Your `Paddle Vendor ID` which can be found on the [Paddle's SDK page](https://vendors.paddle.com/sdk)
* Your `Paddle API key` which is found on the same [Paddle's SDK page](https://vendors.paddle.com/sdk)

At the moment several of the tests also require a few other bits created in Paddle. We are looking at removing these dependencies soon be creating them with fixtures. Please help us do it if you are up for it.

* A `Paddle Product ID` which you can get one by creating a product on [Paddle's product page](https://vendors.paddle.com/products)
* A `Paddle Plan/Subscription ID` which can created on [Paddle's Subscription Plans page](https://vendors.paddle.com/subscriptions/plans)
* A `Paddle Checkout ID` which can be got by going into an order from the [Paddle orders page](https://vendors.paddle.com/orders). If you don't have an orders yet you can create a order for $0.

The tests currently require you to add the above as environmental variables (names below). To make them easier to set these each time the python virtual environment is loaded they can be places into a `.env` file which can be source'd.

```
# Create a file called .env and add the below
export PADDLE_VENDOR_ID=...
export PADDLE_API_KEY="..."
export PADDLE_TEST_DEFAULT_CHECKOUT_ID="..."
export PADDLE_TEST_DEFAULT_PRODUCT_ID=...
export PADDLE_TEST_DEFAULT_PLAN_ID=...

poetry shell
source .env
pytest tests/
# Coverage info is written to htmlcov/
```

All tests are currently run against Paddle's API directly. No mocks are used as this is meant to be a thin wrapper. This does mean you need to set a few environmental variables specific to your Paddle account for the tests to run correctly.


### Cleanup

_(These tests are currently not working and marked as skipped so this can be ignored)_

Parts of the Paddle API have create endpoints but not delete endpoints. Because of this several tests need to be cleaned up manually after they are run:


* `tests/test_licenses.py::test_generate_license`
* `tests/test_pay_links.py::test_create_pay_link`



## Submitting changes

Please send a [GitHub Pull Request to paddle-python](https://github.com/pyepye/paddle-python/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). All changes should have at least one test to accompany it, either to prove the bug it is fixing has indeed been fixed on to ensure a new feature works as expected.

Please follow our coding conventions (below) and try and make all of your commits atomic (one feature per commit) where possible.

## Coding conventions

* We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a guide.
* Please keep to the same style as the code already (single quotes, line length etc).
* We want to keep supporting Python 3.5 for now so no `fstrings` sorry
