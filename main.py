from datetime import datetime


def add_item(owner_name, item_name, size, condition):
    print("\n Добавление вещи ")
    print("Владелец:", owner_name)
    print("Вещь:", item_name)
    print("Размер:", size)
    print("Состояние:", condition)

    if condition.lower() == "новое" or condition.lower() == "хорошее":
        print("Вещь подходит для размещения.")
        return True
    else:
        print("Вещь не может быть размещена для обмена.")
        return False


def check_item_availability(is_available):
    print("\n Проверка доступности ")

    if is_available:
        return "Вещь доступна для обмена."
    else:
        return "Вещь недоступна для обмена."


def create_exchange_request(sender_name, offered_item, requested_item):
    print("\n Создание запроса на обмен ")
    print("Отправитель:", sender_name)
    print("Предлагаемая вещь:", offered_item)
    print("Запрашиваемая вещь:", requested_item)

    if offered_item != requested_item:
        return "Запрос создан."
    else:
        return "Запрос не создан: вещи должны отличаться."


def process_exchange_request(request_status):
    print("\n Обработка запроса ")

    if request_status.lower() == "принят":
        return "Запрос принят. Можно оформить передачу."
    elif request_status.lower() == "отклонён":
        return "Запрос отклонён."
    else:
        return "Запрос ожидает решения."


def create_transfer(sender_name, receiver_name):
    current_time = datetime.now()

    print("\n Передача вещей ")
    print("Отправитель:", sender_name)
    print("Получатель:", receiver_name)
    print("Дата:", current_time.strftime("%d.%m.%Y %H:%M"))

    return "Передача сформирована."


def main():
    print(" Сервис обмена одеждой ")

    owner_name = "Анна"
    item_name = "Джинсовая куртка"
    size = "M"
    condition = "хорошее"

    item_added = add_item(
        owner_name,
        item_name,
        size,
        condition
    )

    print(check_item_availability(item_added))

    if item_added:
        sender_name = "Мария"
        offered_item = "Белая толстовка"

        request_result = create_exchange_request(
            sender_name,
            offered_item,
            item_name
        )

        print(request_result)

        request_status = "принят"

        processing_result = process_exchange_request(request_status)
        print(processing_result)

        if request_status.lower() == "принят":
            transfer_result = create_transfer(
                owner_name,
                sender_name
            )

            print(transfer_result)


if __name__ == "__main__":
    main()