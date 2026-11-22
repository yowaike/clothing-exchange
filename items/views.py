from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ItemFilterForm, ItemForm
from .models import Item


def home(request):
    """Главная страница: каталог с фильтрацией, сортировкой и пагинацией."""
    form = ItemFilterForm(request.GET or None)
    items = Item.objects.filter(is_available=True)

    if form.is_bound and form.is_valid():
        size = form.cleaned_data.get("size")
        condition = form.cleaned_data.get("condition")
        sort_by = form.cleaned_data.get("sort") or "item_name"

        if size:
            items = items.filter(size__icontains=size)
        if condition:
            items = items.filter(condition__icontains=condition)

        allowed_sorts = ["item_name", "-item_name", "size", "condition"]
        if sort_by in allowed_sorts:
            items = items.order_by(sort_by)
        else:
            items = items.order_by("item_name")
    else:
        items = items.order_by("item_name")

    paginator = Paginator(items, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "items/home.html", {
        "page_obj": page_obj,
        "form": form,
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


def item_create(request):
    """Представление для создания новой вещи."""
    if request.method == "POST":
        # Передаём форме данные и файлы (для загрузки изображения)
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("items:home")
    else:
        # При GET-запросе создаём пустую форму с начальными значениями
        form = ItemForm(initial={"is_available": True})

    return render(request, "items/item_form.html", {"form": form})


def item_update(request, item_id):
    """Редактирование существующей вещи."""
    item = get_object_or_404(Item, pk=item_id)

    if request.method == "POST":
        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item,
        )
        if form.is_valid():
            form.save()
            return redirect("items:item_detail", item_id=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "items/item_form.html",
        {
            "form": form,
            "item": item,
        },
    )


@require_POST
def item_delete(request, item_id):
    """Удаление вещи. Выполняется только через POST-запрос."""
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return redirect("items:home")
