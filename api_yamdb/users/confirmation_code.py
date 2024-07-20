import uuid

from django.core.cache import cache


def store_confirmation_code(username, code):
    cache.set(f'confirmation_code_{username}', code, timeout=3600)  # Хранение кода в течение 1 часа


def get_confirmation_code(username):
    return cache.get(f'confirmation_code_{username}')


def generate_confirmation_code():
    return str(uuid.uuid4())


if __name__ == '__main__':
    pass
    # print(get_confirmation_code('Lenadi'))
