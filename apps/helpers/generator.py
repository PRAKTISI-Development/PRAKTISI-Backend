import secrets
import string

def identity_generator():
    """
    Generate a random string of a given length (10).

    Returns:
    - str: Random string.
    """
    alphabet = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphabet) for _ in range(10))
    return random_string

def identity_generator_information():
    """
    Generate a random string of a given length (10).

    Returns:
    - str: Random string.
    """
    alphabet = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphabet) for _ in range(5))
    return random_string
