import secrets
import string

def generate_token():
    alphabet = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(12))
    return token

if __name__ == "__main__":
    print(generate_token())

