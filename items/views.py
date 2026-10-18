
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from storage import load_items


def get_items():
    items_file = Path(settings.BASE_DIR) / "data" / "items.json"
    return load_items(str(items_file))


def home(request):
    items = [
        item for item in get_items()
        if item.is_available
    ]
    return render(request, "items/home.html", {"items": items})


def item_detail(request, item_id):
    items = get_items()
    item = next(
        (item for item in items if item.id == item_id),
        None,
    )

    if item is None:
        raise Http404("Вещь не найдена")

    similar_items = [
        other for other in items
        if other.id != item.id and other.is_available
    ][:5]

    return render(
        request,
        "items/item_detail.html",
        {
            "item": item,
            "similar_items": similar_items,
        },
    )
