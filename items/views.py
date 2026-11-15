from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from .models import Item


def home(request):
    """
    Главная страница: список доступных вещей.
    ORM-аналог: SELECT * FROM items WHERE is_available = 1 ORDER BY item_name
    """
    items = Item.objects.filter(is_available=True).order_by('item_name')
    return render(request, "items/home.html", {"items": items})


def item_detail(request, item_id):
    """
    Страница конкретной вещи.
    ORM-аналог: SELECT * FROM items WHERE id = ? AND is_available = 1
    """
    # get_object_or_404 автоматически вернет страницу 404, если вещь не найдена
    item = get_object_or_404(Item, pk=item_id, is_available=True)

    # Поиск похожих вещей того же размера (исключаем текущую вещь)
    # ORM-аналог: SELECT * FROM items WHERE size = ? AND id != ? AND
    # is_available = 1 LIMIT 5
    similar_items = Item.objects.filter(
        size=item.size,
        is_available=True
    ).exclude(pk=item.pk)[:5]

    return render(
        request,
        "items/item_detail.html",
        {
            "item": item,
            "similar_items": similar_items,
        },
    )


def search_items(request):
    """
    Поиск вещей по названию.
    ORM-аналог: SELECT * FROM items WHERE item_name LIKE '%query%' AND is_available = 1
    """
    query = request.GET.get("q", "").strip()
    items = []

    if query:
        # __icontains обеспечивает регистронезависимый поиск по вхождению строки
        items = Item.objects.filter(
            item_name__icontains=query,
            is_available=True
        ).order_by('item_name')

    return render(request, "items/search.html", {"items": items, "query": query})


def statistics(request):
    """
    Страница статистики: количество вещей у каждого владельца.
    ORM-аналог: SELECT owner__name, COUNT(id) AS items_count FROM items GROUP BY owner__name ORDER BY items_count DESC
    """
    # values('owner__name') группирует по имени владельца (через ForeignKey)
    # annotate добавляет вычисляемое поле items_count
    stats = Item.objects.values('owner__name').annotate(
        items_count=Count('id')
    ).order_by('-items_count')

    return render(request, "items/statistics.html", {"statistics": stats})
