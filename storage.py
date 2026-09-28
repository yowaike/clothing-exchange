# модуль для сохранения и загрузки данных
# используем json, потому что он простой и встроенный

import json
from typing import List, Dict


def load_items(filename: str) -> List[Dict]:
    # загружаем вещи из файла
    # если файла нет или он пустой — возвращаем пустой список
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("файл с вещами не найден, создаём пустой список")
        return []

    except json.JSONDecodeError:
        print("файл повреждён, создаём пустой список")
        return []


def save_items(filename: str, items: List[Dict]) -> None:
    # сохраняем вещи в файл
    # ensure_ascii=False, чтобы русские буквы нормально читались
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def load_exchanges(filename: str) -> List[Dict]:
    # загружаем запросы на обмен из файла
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("файл с запросами не найден, создаём пустой список")
        return []

    except json.JSONDecodeError:
        print("файл повреждён, создаём пустой список")
        return []


def save_exchanges(filename: str, exchanges: List[Dict]) -> None:
    # сохраняем запросы на обмен в файл
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(exchanges, file, ensure_ascii=False, indent=2)
