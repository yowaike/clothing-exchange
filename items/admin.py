from django.contrib import admin
from .models import User, Item, ExchangeRequest


class ExchangeRequestInline(admin.TabularInline):
    """Встроенная форма для отображения заявок на обмен прямо в карточке вещи."""
    model = ExchangeRequest
    extra = 0  # Не показывать пустые формы для добавления по умолчанию
    readonly_fields = ('requester', 'status')  # Запрещаем редактировать заявки из карточки вещи
    can_delete = False  # Запрещаем удаление заявок из карточки вещи


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка отображения пользователей в админке."""
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name',)
    ordering = ('id',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Настройка отображения вещей в админке."""
    list_display = ('id', 'item_name', 'owner', 'size', 'condition', 'is_available')
    list_filter = ('is_available', 'size', 'condition', 'owner')
    search_fields = ('item_name', 'owner__name')
    ordering = ('-id',)
    list_per_page = 20
    inlines = [ExchangeRequestInline]  # Добавляем заявки на обмен внутрь карточки вещи


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    """Настройка отображения заявок на обмен в админке."""
    list_display = ('id', 'item', 'requester', 'status')
    list_filter = ('status',)
    search_fields = ('item__item_name', 'requester__name')
    ordering = ('-id',)
