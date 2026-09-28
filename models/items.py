# класс вещи

from typing import Dict, List, Optional


class Item:
    """Вещь, доступная для обмена."""

    def __init__(self, item_id: int, owner_name: str, item_name: str,
                 size: str, condition: str,
                 is_available: bool = True) -> None:
        # сохраняем данные вещи в атрибутах
        self.id = item_id
        self.owner_name = owner_name
        self.item_name = item_name
        self.size = size
        self.condition = condition
        self.is_available = is_available

    def is_suitable_for_exchange(self) -> bool:
        # проверяем, подходит ли вещь для обмена
        return self.condition.lower() in ("новое", "хорошее")

    def __str__(self) -> str:
        # строковое представление вещи
        status = "доступна" if self.is_available else "недоступна"
        return (
            f"[{self.id}] {self.item_name} "
            f"(размер {self.size}, состояние: {self.condition}, "
            f"владелец: {self.owner_name}) — {status}"
        )

    @classmethod
    def from_data(cls, data: Dict) -> "Item":
        # создаём вещь из словаря (для загрузки из json)
        return cls(
            item_id=data["id"],
            owner_name=data["owner_name"],
            item_name=data["item_name"],
            size=data["size"],
            condition=data["condition"],
            is_available=data["is_available"],
        )

    def to_data(self) -> Dict:
        # превращаем вещь в словарь (для сохранения в json)
        return {
            "id": self.id,
            "owner_name": self.owner_name,
            "item_name": self.item_name,
            "size": self.size,
            "condition": self.condition,
            "is_available": self.is_available,
        }


def add_item(items: List[Item], owner_name: str, item_name: str,
             size: str, condition: str) -> Item:
    # создаём объект Item и добавляем в коллекцию
    item_id = len(items) + 1
    item = Item(item_id, owner_name, item_name, size, condition)
    items.append(item)
    return item


def find_item(items: List[Item], query: str) -> List[Item]:
    # ищем вещи по названию
    query_lower = query.lower()
    result = []

    for item in items:
        if query_lower in item.item_name.lower():
            result.append(item)

    return result


def filter_items_by_size(items: List[Item], size: str) -> List[Item]:
    # отбираем вещи по размеру
    result = []

    for item in items:
        if item.size.lower() == size.lower():
            result.append(item)

    return result


def sort_items(items: List[Item]) -> List[Item]:
    # сортируем по названию через lambda
    return sorted(items, key=lambda item: item.item_name)


def check_item_availability(items: List[Item], item_id: int) -> bool:
    # проверяем, доступна ли вещь
    for item in items:
        if item.id == item_id:
            return item.is_available
    return False


def get_item_by_id(items: List[Item], item_id: int) -> Optional[Item]:
    # находим вещь по id
    for item in items:
        if item.id == item_id:
            return item
    return None


def get_item_by_name(items: List[Item], owner_name: str,
                     item_name: str) -> Optional[Item]:
    # находим вещь по имени владельца и названию
    for item in items:
        if item.owner_name == owner_name and item.item_name == item_name:
            return item
    return None
