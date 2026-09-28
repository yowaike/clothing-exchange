# вспомогательные функции для ввода
# чтобы программа не падала, если пользователь ввёл что-то не то

def input_str(prompt: str) -> str:
    # запрашиваем строку, пока пользователь не введёт что-то непустое
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("ошибка: строка не может быть пустой")


def input_int(prompt: str) -> int:
    # запрашиваем целое число, пока не получится преобразовать
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print("ошибка: введите целое число")

        except KeyboardInterrupt:
            # если нажали ctrl+c — выходим из программы
            print("\nвыход из программы")
            raise
