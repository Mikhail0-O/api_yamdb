from django.core.exceptions import ValidationError

from api_yamdb.settings import ROLE_ADMIN, ROLE_MODERATOR, ROLE_USER


def validate_role(value):
    if value not in [ROLE_USER, ROLE_ADMIN, ROLE_MODERATOR]:
        raise ValidationError(f"{value} - недопустимая роль")


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            f"Использовать имя '{value}' в качестве username запрещено"
        )
