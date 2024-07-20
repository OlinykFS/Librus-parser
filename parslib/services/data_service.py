import os
from cryptography.fernet import Fernet


CREDENTIALS_FILE = 'credentials.enc'


ENCRYPTION_KEY = os.environ.get('LIBRUS_ENCRYPTION_KEY') or Fernet.generate_key()


def save_credentials(username, password):

    credentials = f"{username}:{password}".encode()
    f = Fernet(ENCRYPTION_KEY)
    encrypted_credentials = f.encrypt(credentials)

    with open(CREDENTIALS_FILE, 'wb') as file:
        file.write(encrypted_credentials)


def get_credentials():

    if not os.path.exists(CREDENTIALS_FILE):
        return None

    with open(CREDENTIALS_FILE, 'rb') as file:
        encrypted_credentials = file.read()

    f = Fernet(ENCRYPTION_KEY)
    decrypted_credentials = f.decrypt(encrypted_credentials).decode()
    username, password = decrypted_credentials.split(':')

    return {
        'action': 'login',
        'login': username,
        'pass': password
    }


def clear_credentials():

    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)