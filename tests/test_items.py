# тесты для модуля items

from models.items import (
    Item,
    add_item,
    find_item,
    filter_items_by_size,
    check_item_availability,
)


def test_item_creation():
    # проверяем создание объекта Item
    item = Item(1, "Анна", "Куртка", "M", "хорошее")
    assert item.id == 1
    assert item.owner_name == "Анна"
    assert item.item_name == "Куртка"
    assert item.size == "M"
    assert item.condition == "хорошее"
    assert item.is_available is True


def test_item_is_suitable_for_exchange():
    # проверяем метод проверки состояния
    item = Item(1, "Анна", "Куртка", "M", "хорошее")
    assert item.is_suitable_for_exchange()

    bad_item = Item(2, "Анна", "Куртка", "M", "плохое")
    assert not bad_item.is_suitable_for_exchange()


def test_add_item():
    items = []
    add_item(items, "Анна", "Джинсовая куртка", "M", "хорошее")
    assert len(items) == 1
    assert items[0].item_name == "Джинсовая куртка"


def test_find_item():
    items = []
    add_item(items, "Анна", "Джинсовая куртка", "M", "хорошее")
    add_item(items, "Иван", "Пальто", "L", "отличное")

    result = find_item(items, "куртка")
    assert len(result) == 1
    assert result[0].owner_name == "Анна"


def test_filter_items_by_size():
    items = []
    add_item(items, "Анна", "Куртка", "M", "хорошее")
    add_item(items, "Иван", "Пальто", "L", "отличное")

    result = filter_items_by_size(items, "M")
    assert len(result) == 1


def test_check_item_availability():
    items = []
    add_item(items, "Анна", "Куртка", "M", "хорошее")

    assert check_item_availability(items, 1)
    assert not check_item_availability(items, 99)
