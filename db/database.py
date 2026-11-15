import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
DATA_DIR = BASE_DIR / "data"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Create database tables from the SQL schema."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.executescript(schema)


def load_json(filename):
    """Load data from a JSON file."""
    path = DATA_DIR / filename

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def migrate_json_data():
    """Transfer data from JSON files into SQLite."""
    items = load_json("items.json")
    users = load_json("users.json")
    exchanges = load_json("exchanges.json")

    with get_connection() as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO items
            (id, owner_name, item_name, size, condition, is_available)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["id"],
                    item["owner_name"],
                    item["item_name"],
                    item["size"],
                    item["condition"],
                    int(item["is_available"]),
                )
                for item in items
            ],
        )

        connection.executemany(
            """
            INSERT OR IGNORE INTO users (id, name, email)
            VALUES (?, ?, ?)
            """,
            [
                (user["id"], user["name"], user["email"])
                for user in users
            ],
        )

        connection.executemany(
            """
            INSERT OR IGNORE INTO exchanges
            (id, item_id, requester_id, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    exchange["id"],
                    exchange["item_id"],
                    exchange["requester_id"],
                    exchange["status"],
                )
                for exchange in exchanges
            ],
        )


if __name__ == "__main__":
    print("🔄 Инициализация базы данных (создание таблиц)...")
    init_db()
    print("🔄 Перенос данных из JSON в SQLite...")
    migrate_json_data()
    print("✅ Готово! Данные успешно перенесены.")
