import os
from cryptography.fernet import Fernet


class EncryptionKeyManager:
    key_path = None
    key = None
    cipher = None

    def __init__(self, key_path='encryption_key.key'):
        self.key_path = key_path
        if os.path.exists(self.key_path):
            self.key = self._load_key()
        else:
            self.key = self._generate_key()
        self.cipher = Fernet(self.key)

    def _generate_key(self):
        # Generate a new key and save it to the file
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as key_file:
            key_file.write(key)
        return key

    def _load_key(self):
        with open(self.key_path, "rb") as key_file:
            return key_file.read()

    def encrypt(self, text: str):
        return self.cipher.encrypt(str(text).encode('utf-8'))

    def decrypt(self, token):
        return self.cipher.decrypt(token).decode('utf-8')
