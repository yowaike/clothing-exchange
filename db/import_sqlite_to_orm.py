"""
Скрипт переноса данных из базы ПР7 (SQLite) в базу Django ORM.
Запускать из корня проекта: python db/import_sqlite_to_orm.py
"""
import os
import sys
import sqlite3
from pathlib import Path

import django
from django.db import transaction

# Определяем корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Путь к ИСХОДНОЙ базе ПР7 (созданной вручную)
SOURCE_DB = BASE_DIR / "db" / "clothing_exchange.db"

# Настраиваем Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clothing_exchange.settings")
django.setup()

# Импортируем модели ПОСЛЕ django.setup()
from items.models import User, Item, ExchangeRequest


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    print(f"Источник: {SOURCE_DB}")
    print(f"Цель: база Django ORM (db.sqlite3)")

    with sqlite3.connect(SOURCE_DB) as source_conn:
        source_conn.row_factory = sqlite3.Row

        # Считываем данные из старой базы
        users = source_conn.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()

        items = source_conn.execute(
            "SELECT id, owner_name, item_name, size, condition, is_available "
            "FROM items ORDER BY id"
        ).fetchall()

        exchanges = source_conn.execute(
            "SELECT id, item_id, requester_id, status "
            "FROM exchanges ORDER BY id"
        ).fetchall()

    print(f"Найдено в источнике: "
          f"{len(users)} пользователей, "
          f"{len(items)} вещей, "
          f"{len(exchanges)} обменов")

    # Переносим одной транзакцией
    with transaction.atomic():
        # 1. Пользователи
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "email": row["email"],
                },
            )

        # 2. Вещи (связываем с пользователем по имени владельца)
        for row in items:
            # Находим владельца по имени
            try:
                owner = User.objects.get(name=row["owner_name"])
            except User.DoesNotExist:
                print(f" Владелец '{row['owner_name']}' не найден, "
                      f"вещь '{row['item_name']}' пропускаем")
                continue

            Item.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "owner": owner,
                    "item_name": row["item_name"],
                    "size": row["size"],
                    "condition": row["condition"],
                    "is_available": bool(row["is_available"]),
                },
            )

        # 3. Обмены
        for row in exchanges:
            try:
                item = Item.objects.get(pk=row["item_id"])
                requester = User.objects.get(pk=row["requester_id"])
            except (Item.DoesNotExist, User.DoesNotExist) as e:
                print(f"⚠️  Связанный объект не найден для обмена #{row['id']}: {e}")
                continue

            ExchangeRequest.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "item": item,
                    "requester": requester,
                    "status": row["status"],
                },
            )

    # Итоговая проверка
    print("\nПеренос завершён!")
    print(f"   Пользователей в ORM: {User.objects.count()}")
    print(f"   Вещей в ORM:         {Item.objects.count()}")
    print(f"   Обменов в ORM:       {ExchangeRequest.objects.count()}")


if __name__ == "__main__":
    main()
