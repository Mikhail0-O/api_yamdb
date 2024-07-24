from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидатор для проверки года выхода произведения"""
    if value > timezone.now().year:
        raise ValidationError('Год выхода не может быть больше текущего года.')