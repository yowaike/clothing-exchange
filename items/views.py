from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Item


def home(request):
    """Главная страница: каталог доступных вещей с пагинацией и сортировкой."""
    items = Item.objects.filter(is_available=True)

    sort_by = request.GET.get('sort', 'item_name')
    allowed_sorts = ['item_name', '-item_name', 'size', 'condition']
    if sort_by not in allowed_sorts:
        sort_by = 'item_name'

    items = items.order_by(sort_by)

    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "items/home.html", {
        "page_obj": page_obj,
        "sort_by": sort_by,
    })


def item_detail(request, item_id):
    """Страница конкретной вещи."""
    item = get_object_or_404(
        Item.objects.select_related('owner'),
        pk=item_id,
        is_available=True
    )

    similar_items = Item.objects.filter(
        size=item.size,
        is_available=True
    ).exclude(pk=item.pk).order_by('item_name')[:5]

    return render(
        request,
        "items/item_detail.html",
        {
            "item": item,
            "similar_items": similar_items,
        },
    )


def search_items(request):
    """Поиск вещей по названию или состоянию (использует Q-объекты)."""
    query = request.GET.get("q", "").strip()
    items = []

    if query:
        items = Item.objects.filter(
            Q(item_name__icontains=query) | Q(condition__icontains=query),
            is_available=True
        ).order_by('item_name')

    return render(request, "items/search.html", {"items": items, "query": query})


def statistics(request):
    """Страница статистики с агрегацией и аннотацией."""
    stats = Item.objects.values('owner__name').annotate(
        items_count=Count('id')
    ).order_by('-items_count')

    total_items = Item.objects.filter(is_available=True).count()
    avg_items_per_owner = Item.objects.values('owner__name').annotate(
        count=Count('id')
    ).aggregate(avg=Avg('count'))['avg']

    return render(request, "items/statistics.html", {
        "statistics": stats,
        "total_items": total_items,
        "avg_items_per_owner": round(avg_items_per_owner or 0, 1),
    })