from django.core.exceptions import ValidationError


def validate_role(value):
    if value not in ['user', 'admin', 'moderator']:
        raise ValidationError(f"{value} - недопустимая роль")


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            f"Использовать имя '{value}' в качестве username запрещено"
        )
