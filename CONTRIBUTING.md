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
1. Create a new pull request


## Testing

### Setup

This package uses [Poetry](https://python-poetry.org/) for packaging and dependency management. Before you get started please install it.

```bash
# Fork and clone this repo
poetry install
poetry shell
```

An account in the [Paddle Sandbox](https://sandbox-vendors.paddle.com/authentication) has been created for testing this package and this account has been hardcoded into the tests via the paddle-client fixture so all of the tests will ignore any PADDLE_* environmental variables.

This sandbox account is currently configured in a state that all of the tests pass out of the box including the creation of products and subscriptions which can't be done via the API.
With that in mind, this might not be the case in the future. If a test fails due to missing data, the pytest error should make it clear what data needs to be created. Below are instructions on how to create the test data.


#### Creating a product

This requires access to the Paddle Sandbox account (`paddle-client@pkgdeploy.com`). If you do not have access please create a GitHub issue.

1. Go to the Sandbox products https://sandbox-vendors.paddle.com/products
1. Product Name: `test-product` (the name is used to match the fixture)
1. Fulfillment Method: `Paddle License`
  * Default Activations per License: 9999
  * Enable Trials: Unchecked
  * Default Expiry Days: 0
1. Complete your integration of the Paddle SDK: Ignore Waiting for API requests... (this can be ignored)
1. Set Prices > Go to prices manager
  * USD: $1
  * Sale: Disabled
1. Close the page (without saving)


#### Creating a subscription

Certain tests require a subscription to be created, which is simply a plan that has been paid for by a user. While there is no way to create subscriptions / payment via the Paddle API, a simple way to using the PaddleCheckout has been configured to create them manually in a few seconds:

Before following the below steps to create a payment please run the tests as a payment may already exist. It will also make sure a Paddle plan is setup ready for a subscription and let you know of the plan ID which is needed below.

1. Run a test which requires a subscription payment (to print the Plan ID) - `pytest tests/test_subscription_payments.py::test_list_subscription_payments`
1. Take note of the plan ID from the failed test (if the test does not fail you don't need to setup a new subscription)
1. Edit the PaddleCheckout HTML page at `tests/create_subscription.html` replacing `data-product="<plan-id>"` with the output of the above command:
    ```
    <!-- If the new plan ID was 9000: -->
    <a
      data-product="9000"
      class="paddle_button"
      href="#!"
      ...
    >
      Buy Now!
    </a>
    ```
1. Open the create_subscription checkout HTML page - `open tests/create_subscription.html`
1. Click on the `Buy Now!` button
1. In the Paddle modal enter fake card info provided on the page


## Running tests

Pytest is used to run the tests:

```bash
pytest tests/
# Coverage info is written to htmlcov/
```
All tests are run against the Paddle Sandbox environment and most of the setup and teardown is handled within the tests.

The only exception to this is if someone accidentally deletes all of the subscription plans and products. When this happens it means any test which requires a checkout to have been completed (payments, updates etc) will fail due to no plan or product existing.


### Mocking

As few mocks should be used as possible, Mocks should only be used for dangerous Paddle operations that can't be undone or cleaned up via the API making it difficult to create enough test data..

Mocks should be done at the point paddle-python interfaces with `requests` and check the exact kwargs that were sent. This will cause any change in the request to cause the mocked test to fail. All mocked tests should also be accompanied by a matching test that hits Paddle's API but has the decorator`@pytest.mark.skip()` (see an already mocked test below as an example).

The current mocked tests are:

* Cancel Subscription - `test_subscription_users.py::test_cancel_subscription`


## Coding conventions

* We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a guide
* All code in the paddle module should have type hints (checked by mypy)
* Make sure everything is flake8 compliment
* Use `isort` to sort imports and make them easy to read
* Please keep to the same style as the code already (single quotes, line length etc)


## tox

`tox` is set up to help run `pytest` against each of the supported versions (python 3.6+). It will also ensure the above code conventions are adhered to by running `mypy`, `flake8` and `isort` against your code.

To use tox you first need to follow the test setup above, then run the tox command:
```bash
$ tox
```
_Note: As `tox` runs the test suite multiple times, it is configured to skip any tests which require manual clean up. This may change in the future_


## Submitting changes

Please send a [GitHub Pull Request to paddle-python](https://github.com/paddle-python/paddle-client/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)).

All changes should have at least one test to accompany it, either to prove the bug it is fixing has indeed been fixed on to ensure a new feature works as expected.

Please follow our coding conventions and try and make all of your commits atomic (one feature per commit) where possible.


## Documentation

Documentation is hosted on [Read the Docs](https://paddle-client.readthedocs.io/en/latest/) and can be build by anyone in the [paddle-python Github organisation](https://github.com/paddle-python)

To make sure the docs build they are automatically built on each run of `tox`

If you want to build it manually:

```bash
cd docs
make html
```
