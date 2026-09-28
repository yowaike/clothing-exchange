# класс пользователя

from typing import Dict, List, Optional


class User:
    """Пользователь сервиса обмена одеждой."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        # сохраняем данные пользователя в атрибутах
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        # строковое представление пользователя
        return f"[{self.id}] {self.name} ({self.email})"

    @classmethod
    def from_data(cls, data: Dict) -> "User":
        # создаём пользователя из словаря
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> Dict:
        # превращаем пользователя в словарь
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


def get_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    # находим пользователя по id
    for user in users:
        if user.id == user_id:
            return user
    return None


def add_user(users: List[User], name: str, email: str) -> User:
    # создаём пользователя и добавляем в коллекцию
    user_id = len(users) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user
