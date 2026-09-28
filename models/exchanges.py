# класс запроса на обмен

from typing import Dict, List, Optional
from .items import Item, get_item_by_id
from .users import User


class ExchangeRequest:
    """Запрос на обмен вещи."""

    def __init__(self, request_id: int, item: Item, requester: User,
                 status: str = "active") -> None:
        # запрос хранит ссылки на объект вещи и объект пользователя
        self.id = request_id
        self.item = item
        self.requester = requester
        self.status = status

    def cancel(self) -> None:
        # отменяем запрос — меняем статус, объект не удаляем
        if self.status == "active":
            self.status = "cancelled"

    def get_status_text(self) -> str:
        # возвращаем текст статуса
        if self.status == "active":
            return "запрос активен"
        return "запрос отменён"

    def __str__(self) -> str:
        # строковое представление запроса
        return (
            f"[{self.id}] вещь: {self.item.item_name}, "
            f"от: {self.requester.name}, статус: {self.status}"
        )

    @classmethod
    def from_data(cls, data: Dict, item: Item,
                  requester: User) -> "ExchangeRequest":
        # создаём запрос из словаря, объекты вещи и пользователя
        # передаём снаружи
        return cls(
            request_id=data["id"],
            item=item,
            requester=requester,
            status=data["status"],
        )

    def to_data(self) -> Dict:
        # превращаем запрос в словарь — сохраняем только id
        # связанных объектов
        return {
            "id": self.id,
            "item_id": self.item.id,
            "requester_id": self.requester.id,
            "status": self.status,
        }


def is_item_available_for_exchange(exchanges: List[ExchangeRequest],
                                   item: Item) -> bool:
    # проверяем, нет ли активного запроса на эту вещь
    for exchange in exchanges:
        if exchange.item.id == item.id and exchange.status == "active":
            return False
    return True


def create_exchange_request(exchanges: List[ExchangeRequest],
                            items: List[Item],
                            item_id: int,
                            requester: User) -> Optional[ExchangeRequest]:
    # создаём запрос на обмен
    item = get_item_by_id(items, item_id)

    if item is None:
        print("вещь с таким id не найдена")
        return None

    if not item.is_available:
        print("вещь недоступна для обмена")
        return None

    if not is_item_available_for_exchange(exchanges, item):
        print("на эту вещь уже есть активный запрос")
        return None

    request_id = len(exchanges) + 1
    request = ExchangeRequest(request_id, item, requester)
    exchanges.append(request)
    return request


def cancel_exchange_request(exchanges: List[ExchangeRequest],
                            request_id: int) -> bool:
    # ищем запрос и вызываем у него метод cancel()
    for exchange in exchanges:
        if exchange.id == request_id and exchange.status == "active":
            exchange.cancel()
            return True
    return False


def get_request_status(request: ExchangeRequest) -> str:
    # получаем текст статуса через метод объекта
    return request.get_status_text()


def get_active_requests(
    exchanges: List[ExchangeRequest]
) -> List[ExchangeRequest]:
    # возвращаем только активные запросы
    result = []

    for exchange in exchanges:
        if exchange.status == "active":
            result.append(exchange)

    return result
