from datetime import datetime, timedelta

from .test_paddle import paddle_client  # NOQA: F401


def test_get_webhook_history(paddle_client):  # NOQA: F811
    page = 1
    alerts_per_page = 2
    webhook_history = paddle_client.get_webhook_history(
        page=page, alerts_per_page=alerts_per_page,
    )
    assert webhook_history['current_page'] == page
    assert webhook_history['alerts_per_page'] == alerts_per_page
    assert isinstance(webhook_history['total_pages'], int)
    assert isinstance(webhook_history['total_alerts'], int)
    assert isinstance(webhook_history['query_head'], str)
    datetime.strptime(webhook_history['query_head'], '%Y-%m-%d %H:%M:%S')
    # assert isinstance(webhook_history['query_tail'], str)
    assert len(webhook_history['data']) == alerts_per_page
    for webhook in webhook_history['data']:
        assert isinstance(webhook['id'], int)
        assert isinstance(webhook['alert_name'], str)
        assert isinstance(webhook['status'], str)
        assert isinstance(webhook['created_at'], str)
        datetime.strptime(webhook['created_at'], '%Y-%m-%d %H:%M:%S')
        assert isinstance(webhook['updated_at'], str)
        datetime.strptime(webhook['updated_at'], '%Y-%m-%d %H:%M:%S')
        assert isinstance(webhook['attempts'], int)
        assert isinstance(webhook['fields'], dict)
        assert isinstance(webhook['fields']['event_time'], str)
        datetime.strptime(webhook['fields']['event_time'], '%Y-%m-%d %H:%M:%S')
        assert isinstance(webhook['fields']['status'], str)


def test_get_webhook_history_head_and_tail(paddle_client):  # NOQA: F811
    base_webhook_history = paddle_client.get_webhook_history(
        page=1, alerts_per_page=1,
    )
    base_total_alerts = base_webhook_history['total_alerts']
    webhook = base_webhook_history['data'][0]
    head = datetime.strptime(webhook['created_at'], '%Y-%m-%d %H:%M:%S')

    new_head = head + timedelta(minutes=30)
    new_tail = head - timedelta(minutes=30)
    webhook_history = paddle_client.get_webhook_history(
        query_head=new_head.strftime('%Y-%m-%d %H:%M:%S'),
        query_tail=new_tail,

    )
    base_total_alerts = base_webhook_history['total_alerts']
    total_alerts = webhook_history['total_alerts']
    assert base_total_alerts > total_alerts
    for webhook in webhook_history['data']:
        created = datetime.strptime(webhook['created_at'], '%Y-%m-%d %H:%M:%S')
        assert created < new_head
        assert created > new_tail
