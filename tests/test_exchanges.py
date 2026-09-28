# тесты для модуля exchanges

from models.items import Item
from models.users import User
from models.exchanges import (
    ExchangeRequest,
    create_exchange_request,
    cancel_exchange_request,
    get_request_status,
)


def test_exchange_request_creation():
    # проверяем создание запроса
    item = Item(1, "Анна", "Куртка", "M", "хорошее")
    user = User(1, "Иван", "ivan@example.com")

    request = ExchangeRequest(1, item, user)
    assert request.id == 1
    assert request.item is item
    assert request.requester is user
    assert request.status == "active"


def test_cancel_request():
    # проверяем отмену через метод объекта
    item = Item(1, "Анна", "Куртка", "M", "хорошее")
    user = User(1, "Иван", "ivan@example.com")

    request = ExchangeRequest(1, item, user)
    request.cancel()

    assert request.status == "cancelled"


def test_create_exchange_request():
    # создаём запрос через функцию
    items = [Item(1, "Анна", "Куртка", "M", "хорошее")]
    users = [User(1, "Иван", "ivan@example.com")]
    exchanges = []

    result = create_exchange_request(exchanges, items, 1, users[0])
    assert result is not None
    assert len(exchanges) == 1


def test_duplicate_exchange_forbidden():
    # на одну вещь нельзя создать два активных запроса
    items = [Item(1, "Анна", "Куртка", "M", "хорошее")]
    user1 = User(1, "Иван", "ivan@example.com")
    user2 = User(2, "Пётр", "petr@example.com")
    exchanges = []

    create_exchange_request(exchanges, items, 1, user1)
    result = create_exchange_request(exchanges, items, 1, user2)

    assert result is None


def test_cancel_exchange_request():
    # отменяем через функцию
    items = [Item(1, "Анна", "Куртка", "M", "хорошее")]
    user = User(1, "Иван", "ivan@example.com")
    exchanges = []

    create_exchange_request(exchanges, items, 1, user)
    assert cancel_exchange_request(exchanges, 1)
    assert get_request_status(exchanges[0]) == "запрос отменён"
