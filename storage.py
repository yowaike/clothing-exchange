# модуль для сохранения и загрузки данных
# json хранит словари, а программа работает с объектами

import json
from typing import List

from models.items import Item, get_item_by_id
from models.users import User, get_user_by_id
from models.exchanges import ExchangeRequest


def load_items(filename: str) -> List[Item]:
    # загружаем вещи из файла и превращаем словари в объекты
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Item.from_data(item_data) for item_data in data]

    except FileNotFoundError:
        print("файл с вещами не найден, создаём пустой список")
        return []

    except json.JSONDecodeError:
        print("файл повреждён, создаём пустой список")
        return []


def save_items(filename: str, items: List[Item]) -> None:
    # превращаем объекты в словари и сохраняем
    data = [item.to_data() for item in items]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> List[User]:
    # загружаем пользователей
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [User.from_data(user_data) for user_data in data]

    except FileNotFoundError:
        print("файл с пользователями не найден, создаём пустой список")
        return []

    except json.JSONDecodeError:
        print("файл повреждён, создаём пустой список")
        return []


def save_users(filename: str, users: List[User]) -> None:
    # сохраняем пользователей
    data = [user.to_data() for user in users]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_exchanges(filename: str, items: List[Item],
                   users: List[User]) -> List[ExchangeRequest]:
    # загружаем запросы и восстанавливаем связи с объектами
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("файл с запросами не найден, создаём пустой список")
        return []
    except json.JSONDecodeError:
        print("файл повреждён, создаём пустой список")
        return []

    result = []

    for request_data in data:
        item = get_item_by_id(items, request_data["item_id"])
        requester = get_user_by_id(users, request_data["requester_id"])

        if item is None or requester is None:
            # если связанные объекты не найдены, запрос не создаём
            continue

        request = ExchangeRequest.from_data(request_data, item, requester)
        result.append(request)

    return result


def save_exchanges(filename: str, exchanges: List[ExchangeRequest]) -> None:
    # сохраняем запросы — только идентификаторы связанных объектов
    data = [exchange.to_data() for exchange in exchanges]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
