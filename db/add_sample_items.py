"""Скрипт добавления тестовых вещей в базу данных."""
import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clothing_exchange.settings")
django.setup()

from items.models import User, Item


def add_sample_items():
    """Добавляет тестовые вещи в базу данных."""
    # Получаем существующего пользователя или создаем нового
    user, _ = User.objects.get_or_create(
        name="саша",
        defaults={"email": "sasha@example.com"},
    )

    # Список вещей для добавления
    items_data = [
        {"item_name": "кофта полосатая чб", "size": "M", "condition": "отличное", "is_available": True},
        {"item_name": "джинсы синие классические", "size": "32", "condition": "хорошее", "is_available": True},
        {"item_name": "футболка белая базовая", "size": "S", "condition": "отличное", "is_available": True},
        {"item_name": "куртка джинсовая", "size": "M", "condition": "удовлетворительное", "is_available": True},
        {"item_name": "платье летнее в цветочек", "size": "S", "condition": "отличное", "is_available": True},
        {"item_name": "свитер шерстяной серый", "size": "L", "condition": "хорошее", "is_available": True},
        {"item_name": "юбка миди черная", "size": "M", "condition": "отличное", "is_available": True},
        {"item_name": "рубашка клетчатая", "size": "L", "condition": "хорошее", "is_available": True},
        {"item_name": "пальто бежевое длинное", "size": "M", "condition": "удовлетворительное", "is_available": True},
        {"item_name": "шорты джинсовые", "size": "S", "condition": "отличное", "is_available": True},
    ]

    added_count = 0
    for data in items_data:
        obj, created = Item.objects.get_or_create(
            item_name=data["item_name"],
            defaults={
                "owner": user,
                "size": data["size"],
                "condition": data["condition"],
                "is_available": data["is_available"],
            },
        )
        if created:
            added_count += 1
            print(f"  Добавлено: {data['item_name']} ({data['size']}, {data['condition']})")
        else:
            print(f"  Уже существует: {data['item_name']}")

    print(f"\nГотово! Добавлено новых вещей: {added_count}")
    print(f"Всего вещей в базе: {Item.objects.count()}")


if __name__ == "__main__":
    add_sample_items()
