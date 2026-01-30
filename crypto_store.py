"""
Cryptography and Storage Module
Implements PBKDF2 + Fernet (AES) encryption
File: crypto_store.py
"""

import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class CryptoStore:
    """Handles cryptographic operations and secure data storage"""
    
    def __init__(self, filename="users.json"):
        """Initialize CryptoStore"""
        self.filename = filename
        self.iterations = 100000  # PBKDF2 iterations
    
    def derive_key(self, password, salt):
        """Derive encryption key from password using PBKDF2"""
        if isinstance(salt, str):
            salt = salt.encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data, password):
        """Encrypt data using Fernet (AES-128-CBC + HMAC)"""
        # Generate random salt
        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        
        fernet = Fernet(key)
        json_data = json.dumps(data)
        encrypted = fernet.encrypt(json_data.encode())
        
        # Store salt + encrypted data
        combined = salt + encrypted
        result = base64.b64encode(combined).decode()
        
        return result
    
    def decrypt_data(self, encrypted_data, password):
        """Decrypt data using Fernet (AES-128-CBC + HMAC)"""
        # Decode and extract salt
        combined = base64.b64decode(encrypted_data)
        salt = combined[:16]
        encrypted = combined[16:]
        
        key = self.derive_key(password, salt)
        fernet = Fernet(key)
        
        decrypted = fernet.decrypt(encrypted)
        data = json.loads(decrypted.decode())
        
        return data
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self, users):
        """Save users to file"""
        with open(self.filename, 'w') as f:
            json.dump(users, f, indent=2)