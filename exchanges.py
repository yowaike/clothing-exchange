# модуль для работы с запросами на обмен

from typing import List, Dict, Optional
from items import get_item_by_id


def is_item_available_for_exchange(items: List[Dict], exchanges: List[Dict],
                                   item_id: int) -> bool:
    # проверяем, нет ли уже активного запроса на эту вещь
    for exchange in exchanges:
        if exchange["item_id"] == item_id and exchange["status"] == "active":
            return False

    return True


def create_exchange_request(exchanges: List[Dict], items: List[Dict],
                            item_id: int,
                            requester_name: str) -> Optional[Dict]:
    # создаём запрос на обмен
    item = get_item_by_id(items, item_id)

    if item is None:
        print("вещь с таким id не найдена")
        return None

    if not item["is_available"]:
        print("вещь недоступна для обмена")
        return None

    if not is_item_available_for_exchange(items, exchanges, item_id):
        print("на эту вещь уже есть активный запрос")
        return None

    request_id = len(exchanges) + 1

    request = {
        "id": request_id,
        "item_id": item_id,
        "requester_name": requester_name,
        "status": "active",
    }

    exchanges.append(request)
    return request


def cancel_exchange_request(exchanges: List[Dict], request_id: int) -> bool:
    # отменяем запрос
    for exchange in exchanges:
        if exchange["id"] == request_id and exchange["status"] == "active":
            exchange["status"] = "cancelled"
            return True

    return False


def get_request_status(request: Dict) -> str:
    # возвращаем текст статуса запроса
    if request["status"] == "active":
        return "запрос активен"
    else:
        return "запрос отменён"


def get_active_requests(exchanges: List[Dict]) -> List[Dict]:
    # возвращаем только активные запросы
    result = []

    for exchange in exchanges:
        if exchange["status"] == "active":
            result.append(exchange)

    return result
