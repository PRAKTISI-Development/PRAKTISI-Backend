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
    return str(random_string)

# Example usage:
random_string = identity_generator()
print(random_string)
