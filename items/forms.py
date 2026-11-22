from django import forms
from django.core.exceptions import ValidationError

from .models import Item


class ItemFilterForm(forms.Form):
    """Форма фильтрации каталога вещей (GET-запрос)."""
    size = forms.CharField(
        required=False,
        label="Размер",
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Например: M, 42",
        }),
    )
    condition = forms.CharField(
        required=False,
        label="Состояние",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Например: отличное",
        }),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("item_name", "По названию"),
            ("-item_name", "По названию (обратно)"),
            ("size", "По размеру"),
            ("condition", "По состоянию"),
        ],
    )


class ItemForm(forms.ModelForm):
    """Форма создания и редактирования вещи (POST-запрос)."""

    class Meta:
        model = Item
        fields = [
            "owner",
            "item_name",
            "size",
            "condition",
            "is_available",
            "image",
        ]
        labels = {
            "owner": "Владелец",
            "item_name": "Название вещи",
            "size": "Размер",
            "condition": "Состояние",
            "is_available": "Доступна для обмена",
            "image": "Фотография",
        }
        help_texts = {
            "item_name": "Укажите уникальное название, например: 'Джинсы синие классические'.",
            "size": "Международный (S, M, L) или цифровой (42, 44) размер.",
            "image": "Загрузите фото в формате JPG или PNG. Максимум 5 МБ.",
        }
        widgets = {
            "owner": forms.Select(attrs={"class": "form-control"}),
            "item_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название вещи",
            }),
            "size": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например: M",
            }),
            "condition": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например: отличное",
            }),
            "is_available": forms.CheckboxInput(
                attrs={"class": "form-check-input"},
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"},
            ),
        }

    def clean_item_name(self):
        """Дополнительная проверка поля названия."""
        name = self.cleaned_data.get("item_name", "").strip()
        if not name:
            raise ValidationError("Название вещи не может быть пустым.")
        if len(name) < 2:
            raise ValidationError(
                "Название должно содержать минимум 2 символа."
            )
        return name

    def clean(self):
        """Проверка взаимосвязанных полей: уникальность вещи у владельца."""
        cleaned_data = super().clean()
        owner = cleaned_data.get("owner")
        item_name = cleaned_data.get("item_name")

        if owner and item_name:
            # Исключаем текущий объект при редактировании,
            # чтобы проверка не считала запись конфликтующей с собой.
            queryset = Item.objects.filter(
                owner=owner,
                item_name__iexact=item_name,
            )
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise ValidationError(
                    f"У пользователя {owner.name} уже есть вещь "
                    f"с названием «{item_name}»."
                )

        return cleaned_data
