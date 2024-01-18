import re


def validate_email(email):
    if len(email) > 7:
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None:
            return True
    return False


def validate_username(username):
    if len(username) > 3:
        if re.match(r"^[a-zA-Z0-9_.-]+$", username) is not None:
            return True
    return False
