import uuid

from django.core.cache import cache

from api_yamdb.settings import TIMEOUT_CONFIRMATION_CODE


def store_confirmation_code(username, code):
    cache.set(
        f'confirmation_code_{username}',
        code, timeout=TIMEOUT_CONFIRMATION_CODE
    )


def get_confirmation_code(username):
    return cache.get(f'confirmation_code_{username}')


def generate_confirmation_code():
    return str(uuid.uuid4())
