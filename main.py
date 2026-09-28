# главный файл программы
# тут собираем всё вместе и запускаем меню

from items import (
    add_item,
    find_item,
    filter_items_by_size,
    sort_items,
)
from exchanges import (
    create_exchange_request,
    cancel_exchange_request,
    get_active_requests,
)
from storage import (
    load_items,
    save_items,
    load_exchanges,
    save_exchanges,
)
from utils import input_str, input_int


def show_items(items: list) -> None:
    # выводим список вещей
    if not items:
        print("список вещей пуст")
        return

    for item in items:
        status = "доступна" if item["is_available"] else "недоступна"
        print(
            f"[{item['id']}] {item['item_name']} "
            f"(размер {item['size']}, состояние: {item['condition']}, "
            f"владелец: {item['owner_name']}) — {status}"
        )


def show_exchanges(exchanges: list) -> None:
    # выводим список запросов
    if not exchanges:
        print("список запросов пуст")
        return

    for ex in exchanges:
        print(
            f"[{ex['id']}] вещь id={ex['item_id']}, "
            f"от: {ex['requester_name']}, статус: {ex['status']}"
        )


def main() -> None:
    # загружаем данные из файлов
    items = load_items("data/items.json")
    exchanges = load_exchanges("data/exchanges.json")

    while True:
        print("\n=== сервис обмена одеждой ===")
        print("1. показать все вещи")
        print("2. найти вещь по названию")
        print("3. фильтр по размеру")
        print("4. сортировать вещи")
        print("5. добавить вещь")
        print("6. создать запрос на обмен")
        print("7. отменить запрос")
        print("8. показать запросы")
        print("0. выход")

        choice = input_int("выберите действие: ")

        if choice == 1:
            show_items(items)

        elif choice == 2:
            query = input_str("введите название: ")
            show_items(find_item(items, query))

        elif choice == 3:
            size = input_str("введите размер: ")
            show_items(filter_items_by_size(items, size))

        elif choice == 4:
            show_items(sort_items(items))

        elif choice == 5:
            owner = input_str("имя владельца: ")
            name = input_str("название вещи: ")
            size = input_str("размер: ")
            condition = input_str("состояние: ")

            add_item(items, owner, name, size, condition)
            print("вещь добавлена")

        elif choice == 6:
            item_id = input_int("id вещи: ")
            requester = input_str("ваше имя: ")

            result = create_exchange_request(exchanges, items, item_id, requester)

            if result:
                print(f"запрос создан, id запроса: {result['id']}")
            else:
                print("не удалось создать запрос")

        elif choice == 7:
            request_id = input_int("id запроса: ")

            if cancel_exchange_request(exchanges, request_id):
                print("запрос отменён")
            else:
                print("запрос не найден или уже отменён")

        elif choice == 8:
            show_exchanges(get_active_requests(exchanges))

        elif choice == 0:
            # сохраняем данные перед выходом
            save_items("data/items.json", items)
            save_exchanges("data/exchanges.json", exchanges)
            print("данные сохранены, выход")
            break

        else:
            print("неверный выбор")


if __name__ == "__main__":
    main()
