from random import choice
from string import ascii_uppercase


def generate_big_header():
    return ''.join(choice(ascii_uppercase) for i in range(32000))
