# тесты для модуля users

from models.users import User, add_user, get_user_by_id


def test_user_creation():
    # проверяем создание пользователя
    user = User(1, "Иван", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван"
    assert user.email == "ivan@example.com"


def test_add_user():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    assert len(users) == 1
    assert users[0].name == "Иван"


def test_get_user_by_id():
    users = []
    add_user(users, "Иван", "ivan@example.com")

    user = get_user_by_id(users, 1)
    assert user is not None
    assert user.name == "Иван"

    missing = get_user_by_id(users, 99)
    assert missing is None
