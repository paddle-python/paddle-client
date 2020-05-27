# How to contribute

Thanks for wanting to contribute to the Paddle python API wrapper. This wrapper is intended to be a 'thin' wrapper around the API and includes no business logic.

Important Paddle resources:

  * [Paddle's Vendors Dashboard](https://vendors.paddle.com/overview) - Please make sure you have registered before you get started
  * [Paddle developer API reference](https://developer.paddle.com/api-reference/intro)


Python resources:

  * [Poetry](https://python-poetry.org/) for python packaging and dependency management
  * [Mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
  * [pytest](https://docs.pytest.org/en/latest/) for running test
  * [isort](https://timothycrosley.github.io/isort/) to keep all our imports looking nice and easy to read
  * [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)


## Summary

Please see the sections below for more details

1. Fork this repo
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Make your code changes and write your tests
1. Ensure all the tests pass (`pytest tests/`)
1. check all coding conventions are adhered to (`tox`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create new pull request


## Setup

This package uses the [Poetry](https://python-poetry.org/) for packaging and dependency management. Before you get started please install it.

Once you have cloned this repository you will then need:
* Your `Paddle Vendor ID` which can be found on the [Paddle's SDK page](https://vendors.paddle.com/sdk)
* Your `Paddle API key` which is found on the same [Paddle's SDK page](https://vendors.paddle.com/sdk)

```bash
# Fork and clone this repo
poetry install

# Create a file called .env and add the above settings
export PADDLE_VENDOR_ID=...
export PADDLE_API_KEY="..."

poetry shell
source .env
```


## Running tests

At the moment several of the tests require a few extra bits of information from Paddle. We are looking at removing these dependencies soon be creating them with fixtures. Please help us do it if you are up for it.

* A `Paddle Product ID` which you can get one by creating a product on [Paddle's product page](https://vendors.paddle.com/products)
* A `Paddle Plan/Subscription ID` which can be created on [Paddle's Subscription Plans page](https://vendors.paddle.com/subscriptions/plans)
* A `Paddle Checkout ID` which can be got by going into an order from the [Paddle orders page](https://vendors.paddle.com/orders). If you don't have any orders yet you can create an order for $0.

The tests currently require you to add the above as environmental variables (names below). To make them easier to set these each time the python virtual environment is loaded they can be placed into a `.env` file which can be sourced.

```bash
# Add the above to the relevant environmental variables (and .env file)
export PADDLE_TEST_DEFAULT_CHECKOUT_ID="..."
export PADDLE_TEST_DEFAULT_PRODUCT_ID=...
export PADDLE_TEST_DEFAULT_PLAN_ID=...

poetry shell
source .env
pytest tests/
# Coverage info is written to htmlcov/
```

### Mocking

As few mocks should be used as possible, Mocks should only be used for dangerous Paddle operations that can't be undone or cleaned up.

Mocks should be done at the point paddle-python interfaces with `requests` and check the exact kwargs that were sent. This will cause any change in the request to cause the mocked test to fail. All mocked tests should also include a commented out function
which will call the actual Paddle endpoint if uncommented (see an already mocked test below as an example).

The current mocked tests are:
* Refund Payment - `test_transactions::test_refund_payment`


### Cleanup

_(These tests are currently not working and marked as skipped so this can be ignored)_

Parts of the Paddle API have create endpoints but not delete endpoints. Because of this several tests need to be cleaned up manually after they are run:


* `tests/test_licenses.py::test_generate_license`
* `tests/test_pay_links.py::test_create_pay_link`


If you want to run `pytest` without running the tests that need manual clean up you can use
```bash
pytest -m "not manual_cleanup" tests/
```

## Coding conventions

* We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a guide
* All code in the paddle module should have type hints (checked by mypy)
* Make sure everything is flake8 compliment
* Use `isort` to sort imports and make them easy to read
* We want to keep supporting Python 3.5 for now so no `fstrings` sorry
* Please keep to the same style as the code already (single quotes, line length etc)


## tox

`tox` is set up to help run `pytest` against each of the supported versions (python 3.5+). It will also ensure the above code conventions are adhered to by running `mypy`, `flake8` and `isort` against your code.

To use tox you first need to follow the test setup above, then run the tox command:
```bash
$ tox
```
_Note: As `tox` runs the test suite multiple times, it is configured to skip any tests which require manual clean up. This may change in the future_


## Submitting changes

Please send a [GitHub Pull Request to paddle-python](https://github.com/pyepye/paddle-python/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)).

All changes should have at least one test to accompany it, either to prove the bug it is fixing has indeed been fixed on to ensure a new feature works as expected.

Please follow our coding conventions and try and make all of your commits atomic (one feature per commit) where possible.
