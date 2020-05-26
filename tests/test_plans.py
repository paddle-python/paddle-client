import os

from .test_paddle import paddle_client  # NOQA: F401


def test_list_plans(paddle_client):  # NOQA: F811
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


def test_list_plans_with_plan(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
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
