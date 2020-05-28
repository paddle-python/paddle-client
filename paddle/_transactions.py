import logging
from typing import List, Union
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def list_transactions(
    self,
    entity: str,
    entity_id: Union[str, int],
    page: int = None
) -> List[dict]:
    """
    https://developer.paddle.com/api-reference/product-api/transactions/listtransactions
    """
    valid_entities = ['user', 'subscription', 'order', 'checkout', 'product']
    if entity not in valid_entities:
        error = 'entity "{0}" must be one of {1}'.format(
            entity, ",".join(valid_entities)
        )
        raise ValueError(error)

    url = '{entity}/{id}/transactions'.format(entity=entity, id=entity_id)
    url = urljoin(self.vendors_v2, url)

    if page:
        return self.post(url=url, json={'page': page})

    return self.post(url=url)
