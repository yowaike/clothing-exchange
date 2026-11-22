from django.db import models


class User(models.Model):
    """Пользователь сервиса обмена."""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Email")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Item(models.Model):
    """Вещь, доступная для обмена."""
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name="Владелец"
    )
    item_name = models.CharField(max_length=200, verbose_name="Название вещи")
    size = models.CharField(max_length=10, verbose_name="Размер")
    condition = models.CharField(max_length=50, verbose_name="Состояние")
    is_available = models.BooleanField(default=True, verbose_name="Доступна для обмена")
    image = models.ImageField(
        upload_to="items/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"


class ExchangeRequest(models.Model):
    """Заявка на обмен вещи."""
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('cancelled', 'Отменен'),
        ('completed', 'Завершен'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="exchange_requests",
        verbose_name="Вещь"
    )
    requester = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="requests",
        verbose_name="Заявитель"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заявка на {self.item.item_name} от {self.requester.name}"

    class Meta:
        verbose_name = "Заявка на обмен"
        verbose_name_plural = "Заявки на обмен"
