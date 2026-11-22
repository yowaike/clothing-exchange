```markdown
# Сервис обмена одеждой «Круговорот вещей»

Веб-приложение для обмена одеждой, позволяющее находить новые вещи и продлевать срок их использования. Проект разрабатывается в рамках дисциплины «Технологии разработки приложений на базе фреймворков».

## Технологии
- Python 3.14, Django 6.1, SQLite
- Django ORM, Django Forms, Django Debug Toolbar
- HTML, CSS, JavaScript, JSON
- pytest, flake8, Pillow

## Структура проекта
```text
clothing-exchange/
├── clothing_exchange/     # настройки Django и корневые URL-маршруты
├── items/                 # основное приложение
│   ├── migrations/        # миграции базы данных
│   ├── static/items/      # CSS, JavaScript и изображения
│   ├── templates/items/   # HTML-шаблоны
│   ├── models.py          # модели User, Item, ExchangeRequest
│   ├── views.py           # представления страниц
│   ├── urls.py            # маршруты приложения
│   ├── forms.py           # классы форм (Form, ModelForm)
│   └── admin.py           # настройка административной панели
├── models/                # классы предметной области предыдущих работ
├── data/                  # исходные данные JSON
├── db/                    # работа с базой данных (database.py, import_sqlite_to_orm.py)
├── sql/                   # SQL-файлы практической работы №7
├── tests/                 # автоматические тесты
├── manage.py              # утилита управления Django
└── README.md              # описание проекта
```

## Модели данных
- **User**: `id`, `name`, `email` (уникальный).
- **Item**: `id`, `owner` (ForeignKey), `item_name`, `size`, `condition`, `is_available`, `image` (ImageField).
- **ExchangeRequest**: `id`, `item` (ForeignKey), `requester` (ForeignKey), `status`.

## Реализованные страницы
- **Главная (`/`)**: каталог с пагинацией, фильтрацией и сортировкой.
- **Карточка вещи (`/items/<id>/`)**: детальная информация, похожие предложения и управление вещью.
- **Поиск (`/search/`)**: поиск по названию или состоянию (без учета регистра).
- **Статистика (`/statistics/`)**: агрегированные данные по владельцам.
- **Административная панель (`/admin/`)**: управление данными с inline-формами и фильтрами.

## Этапы разработки и работа с данными
1. **ПР7 (SQLite)**: прямые SQL-запросы. Файлы `sql/` и `db/database.py` сохранены как история.
2. **ПР9 (Django ORM)**: переход на модели, миграции и ORM-запросы (`filter`, `exclude`, `annotate`, `select_related`). Скрипт `db/import_sqlite_to_orm.py` для переноса данных.
3. **ПР10 (Admin)**: кастомизация списков, фильтров и inline-форм в админке, анализ запросов через Debug Toolbar.
4. **ПР11 (Forms)**: формы фильтрации (`forms.Form`) и создания/редактирования (`ModelForm`). Реализована серверная валидация (`clean`, `clean_<field>`), защита CSRF, удаление через POST-запрос и загрузка изображений (`MEDIA_ROOT`, `MEDIA_URL`).

### Примеры ORM-запросов
```python
# Фильтрация и сортировка
Item.objects.filter(is_available=True).order_by('item_name')

# Поиск по нескольким полям (Q-объекты)
Item.objects.filter(Q(item_name__icontains=query) | Q(condition__icontains=query))

# Агрегация и группировка
Item.objects.values('owner__name').annotate(items_count=Count('id')).order_by('-items_count')
```

## Установка и запуск
1. Клонировать репозиторий и перейти в папку:
   ```powershell
   git clone <адрес_репозитория>
   cd clothing-exchange
   ```
2. Создать и активировать виртуальное окружение:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Установить зависимости:
   ```powershell
   pip install -r requirements.txt
   ```
4. Применить миграции и перенести данные (опционально):
   ```powershell
   python manage.py migrate
   python db/import_sqlite_to_orm.py
   ```
5. Создать суперпользователя и запустить сервер:
   ```powershell
   python manage.py createsuperuser
   python manage.py runserver
   ```
6. Открыть в браузере: `http://127.0.0.1:8000/` и `http://127.0.0.1:8000/admin/`

## Проверка проекта
```powershell
# Проверка конфигурации Django
python manage.py check

# Проверка состояния миграций
python manage.py showmigrations

# Запуск автоматических тестов
python -m pytest -v

# Проверка качества кода
python -m flake8 . --extend-exclude=venv,.venv,__pycache__,items/migrations
```
```