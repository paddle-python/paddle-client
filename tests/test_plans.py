from datetime import datetime

import pytest

from .fixtures import create_plan, paddle_client  # NOQA: F401


def test_list_plans(paddle_client, create_plan):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    plan_list = paddle_client.list_plans()
    for plan in plan_list:
        assert isinstance(plan['id'], int)
        assert isinstance(plan['billing_period'], int)
        assert isinstance(plan['billing_type'], str)
        assert isinstance(plan['initial_price'], dict)
        assert isinstance(plan['name'], str)
        assert isinstance(plan['recurring_price'], dict)
        assert isinstance(plan['trial_days'], int)


def test_list_plans_with_plan_kwarg(paddle_client, create_plan):  # NOQA: F811
    plan_id = create_plan['id']
    plan_list = paddle_client.list_plans(plan=plan_id)
    assert len(plan_list) == 1
    plan = plan_list[0]
    assert plan['id'] == plan_id
    assert isinstance(plan['billing_period'], int)
    assert isinstance(plan['billing_type'], str)
    assert isinstance(plan['initial_price'], dict)
    assert isinstance(plan['name'], str)
    assert isinstance(plan['recurring_price'], dict)
    assert isinstance(plan['trial_days'], int)


def test_get_plan(paddle_client, create_plan):  # NOQA: F811
    plan_id = create_plan['id']
    plan = paddle_client.get_plan(plan=plan_id)
    assert plan['id'] == plan_id
    assert isinstance(plan['billing_period'], int)
    assert isinstance(plan['billing_type'], str)
    assert isinstance(plan['initial_price'], dict)
    assert isinstance(plan['name'], str)
    assert isinstance(plan['recurring_price'], dict)
    assert isinstance(plan['trial_days'], int)


@pytest.mark.manual_cleanup
def test_create_plan(paddle_client):  # NOQA: F811
    now = datetime.now().isoformat()
    plan_name = 'paddle-python-test_create_plan {0}'.format(now)
    plan_trial_days = 999
    plan_length = 999
    plan_type = 'year'
    main_currency_code = 'USD'
    initial_price_usd = 0.0
    initial_price_gbp = 0.0
    initial_price_eur = 0.0
    recurring_price_usd = 0.0
    recurring_price_gbp = 0.0
    recurring_price_eur = 0.0
    response = paddle_client.create_plan(
        plan_name=plan_name,
        plan_trial_days=plan_trial_days,
        plan_length=plan_length,
        plan_type=plan_type,
        main_currency_code=main_currency_code,
        initial_price_usd=initial_price_usd,
        initial_price_gbp=initial_price_gbp,
        initial_price_eur=initial_price_eur,
        recurring_price_usd=recurring_price_usd,
        recurring_price_gbp=recurring_price_gbp,
        recurring_price_eur=recurring_price_eur,
    )
    assert isinstance(response['product_id'], int)
    plan_id = response['product_id']

    plan_list = paddle_client.list_plans(plan=plan_id)
    plan = plan_list[0]
    assert plan['name'] == plan_name
    assert plan['trial_days'] == plan_trial_days
    assert plan['billing_period'] == plan_length
    assert plan['billing_type'] == plan_type

    assert plan['initial_price'] == {
        'USD': '%.2f' % round(initial_price_usd, 2),
        'GBP': '%.2f' % round(initial_price_gbp, 2),
        'EUR': '%.2f' % round(initial_price_eur, 2),
    }
    assert plan['recurring_price'] == {
        'USD': '%.2f' % round(recurring_price_usd, 2),
        'GBP': '%.2f' % round(recurring_price_gbp, 2),
        'EUR': '%.2f' % round(recurring_price_eur, 2),
    }


@pytest.mark.parametrize(
    'currency,missing_field',
    [
        ('USD', 'initial_price_usd'),
        ('USD', 'recurring_price_usd'),
        ('GBP', 'initial_price_gbp'),
        ('GBP', 'recurring_price_gbp'),
        ('EUR', 'initial_price_eur'),
        ('EUR', 'recurring_price_eur'),
    ]
)
def test_create_plan_missing_price(paddle_client, currency, missing_field):  # NOQA: F811, E501
    plan = {
        'plan_name': 'test_create_plan_mmissing_usd_initial',
        'plan_trial_days': 999,
        'plan_length': 999,
        'plan_type': 'year',
        'main_currency_code': currency,
        'initial_price_usd': 0.0,
        'initial_price_gbp': 0.0,
        'initial_price_eur': 0.0,
        'recurring_price_usd': 0.0,
        'recurring_price_gbp': 0.0,
        'recurring_price_eur': 0.0,
    }
    del plan[missing_field]
    with pytest.raises(ValueError) as error:
        paddle_client.create_plan(**plan)

    message = r'main_currency_code is {0} so {1} must be set'
    error.match(message.format(currency, missing_field))
