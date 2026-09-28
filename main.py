# главный файл программы

from models.items import (
    add_item,
    find_item,
    filter_items_by_size,
    sort_items,
)
from models.users import add_user, get_user_by_id
from models.exchanges import (
    create_exchange_request,
    cancel_exchange_request,
    get_active_requests,
)
from storage import (
    load_items,
    save_items,
    load_users,
    save_users,
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
        # у объекта Item есть __str__, поэтому просто print(item)
        print(item)


def show_exchanges(exchanges: list) -> None:
    # выводим список запросов
    if not exchanges:
        print("список запросов пуст")
        return

    for exchange in exchanges:
        print(exchange)


def main() -> None:
    # загружаем данные из файлов
    items = load_items("data/items.json")
    users = load_users("data/users.json")
    exchanges = load_exchanges("data/exchanges.json", items, users)

    while True:
        print("\n=== сервис обмена одеждой ===")
        print("1. показать все вещи")
        print("2. найти вещь по названию")
        print("3. фильтр по размеру")
        print("4. сортировать вещи")
        print("5. добавить вещь")
        print("6. добавить пользователя")
        print("7. создать запрос на обмен")
        print("8. отменить запрос")
        print("9. показать запросы")
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
            name = input_str("имя пользователя: ")
            email = input_str("email: ")
            add_user(users, name, email)
            print("пользователь добавлен")

        elif choice == 7:
            item_id = input_int("id вещи: ")
            requester_id = input_int("id пользователя: ")

            requester = get_user_by_id(users, requester_id)
            if requester is None:
                print("пользователь с таким id не найден")
                continue

            result = create_exchange_request(exchanges, items, item_id, requester)

            if result:
                print(f"запрос создан, id запроса: {result.id}")
            else:
                print("не удалось создать запрос")

        elif choice == 8:
            request_id = input_int("id запроса: ")

            if cancel_exchange_request(exchanges, request_id):
                print("запрос отменён")
            else:
                print("запрос не найден или уже отменён")

        elif choice == 9:
            show_exchanges(get_active_requests(exchanges))

        elif choice == 0:
            # сохраняем всё перед выходом
            save_items("data/items.json", items)
            save_users("data/users.json", users)
            save_exchanges("data/exchanges.json", exchanges)
            print("данные сохранены, выход")
            break

        else:
            print("неверный выбор")


if __name__ == "__main__":
    main()
