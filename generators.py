import random
import string


def generate_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
