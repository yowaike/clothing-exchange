# тесты для модуля exchanges

from items import add_item
from exchanges import (
    create_exchange_request,
    cancel_exchange_request,
    get_request_status,
)


def test_create_exchange_request():
    items = []
    exchanges = []

    add_item(items, "Анна", "Куртка", "M", "хорошее")

    result = create_exchange_request(exchanges, items, 1, "Иван")
    assert result is not None
    assert len(exchanges) == 1


def test_duplicate_exchange_forbidden():
    items = []
    exchanges = []

    add_item(items, "Анна", "Куртка", "M", "хорошее")

    create_exchange_request(exchanges, items, 1, "Иван")
    result = create_exchange_request(exchanges, items, 1, "Пётр")

    assert result is None


def test_cancel_exchange_request():
    items = []
    exchanges = []

    add_item(items, "Анна", "Куртка", "M", "хорошее")
    create_exchange_request(exchanges, items, 1, "Иван")

    assert cancel_exchange_request(exchanges, 1)
    assert get_request_status(exchanges[0]) == "запрос отменён"
