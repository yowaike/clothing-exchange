from django.http import Http404
from django.shortcuts import render

from db.database import get_connection


def home(request):
    """Главная страница: список доступных вещей."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, owner_name, item_name, size, condition, is_available
            FROM items
            WHERE is_available = 1
            ORDER BY item_name
        """).fetchall()

    return render(request, "items/home.html", {"items": rows})


def item_detail(request, item_id):
    """Страница конкретной вещи."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, owner_name, item_name, size, condition, is_available
            FROM items
            WHERE id = ?
        """, (item_id,)).fetchone()

    if row is None or row["is_available"] == 0:
        raise Http404("Вещь не найдена или недоступна для обмена")

    with get_connection() as conn:
        similar_rows = conn.execute("""
            SELECT id, owner_name, item_name, size, condition
            FROM items
            WHERE size = ? AND id != ? AND is_available = 1
            LIMIT 5
        """, (row["size"], row["id"])).fetchall()

    return render(
        request,
        "items/item_detail.html",
        {
            "item": row,
            "similar_items": similar_rows,
        },
    )


def search_items(request):
    """Поиск вещей по названию (параметризованный SQL-запрос с LIKE)."""
    query = request.GET.get("q", "").strip()
    items = []

    if query:
        with get_connection() as conn:
            search_term = f"%{query}%"
            items = conn.execute(
                """
                SELECT id, owner_name, item_name, size, condition, is_available
                FROM items
                WHERE item_name LIKE ? AND is_available = 1
                ORDER BY item_name
                """,
                (search_term,),
            ).fetchall()

    return render(request, "items/search.html", {"items": items, "query": query})


def statistics(request):
    """Страница статистики: количество вещей у каждого владельца (GROUP BY, COUNT)."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT owner_name, COUNT(id) AS items_count
            FROM items
            GROUP BY owner_name
            ORDER BY items_count DESC
        """).fetchall()

    return render(request, "items/statistics.html", {"statistics": rows})
