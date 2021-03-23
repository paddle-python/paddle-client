from .fixtures import (  # NOQA: F401
    create_plan, get_subscription, paddle_client
)


def test_refund_product_payment(paddle_client, get_subscription):  # NOQA: F811,E501
    """
    If you get the error:
        "Paddle error 172 - The transaction can no longer be refunded.""
    You will need to create a new payment. See Creating a subscription in
    CONTRIButiNG.md for instructions
    """
    subscription_list = paddle_client.list_transactions(
        entity='subscription',
        entity_id=get_subscription['subscription_id'],
    )
    response = paddle_client.refund_product_payment(
        order_id=subscription_list[0]['order_id'],
        amount=0.01,
        reason='paddle-python-test_refund_product_payment'
    )
    assert isinstance(response['refund_request_id'], int)
