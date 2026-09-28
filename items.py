# модуль для работы с вещами
# тут храним список вещей и функции для работы с ним

from typing import List, Dict, Optional


def add_item(items: List[Dict], owner_name: str, item_name: str,
             size: str, condition: str) -> Dict:
    # добавляем новую вещь в список
    # id берём как следующий номер
    item_id = len(items) + 1

    item = {
        "id": item_id,
        "owner_name": owner_name,
        "item_name": item_name,
        "size": size,
        "condition": condition,
        "is_available": True,
    }

    items.append(item)
    return item


def find_item(items: List[Dict], query: str) -> List[Dict]:
    # ищем вещи по названию
    # ищем без учёта регистра, чтобы "куртка" и "Куртка" находились одинаково
    query_lower = query.lower()
    result = []

    for item in items:
        if query_lower in item["item_name"].lower():
            result.append(item)

    return result


def filter_items_by_size(items: List[Dict], size: str) -> List[Dict]:
    # отбираем вещи по размеру
    result = []

    for item in items:
        if item["size"].lower() == size.lower():
            result.append(item)

    return result


def sort_items(items: List[Dict]) -> List[Dict]:
    # сортируем вещи по названию
    # используем lambda, чтобы не писать отдельную функцию
    return sorted(items, key=lambda item: item["item_name"])


def check_item_availability(items: List[Dict], item_id: int) -> bool:
    # проверяем, доступна ли вещь для обмена
    for item in items:
        if item["id"] == item_id:
            return item["is_available"]

    return False


def get_item_by_id(items: List[Dict], item_id: int) -> Optional[Dict]:
    # находим вещь по id
    # если не нашли — возвращаем None
    for item in items:
        if item["id"] == item_id:
            return item

    return None
