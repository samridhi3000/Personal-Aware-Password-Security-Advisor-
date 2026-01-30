"""
Authentication Module - Web Version
Handles user signup, login, and OTP generation
File: auth.py
"""

import hashlib
import secrets
import random


class AuthManager:
    def __init__(self, crypto_store):
        """Initialize Authentication Manager"""
        self.crypto = crypto_store
        self.users = self.crypto.load_users()
        self.current_otp = None
        self.session_passwords = {}  # Store passwords during session
    
    def hash_password(self, password, salt):
        """Hash password with salt using SHA256"""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def signup(self, username, password):
        """Create new user account"""
        if username in self.users:
            return {"success": False, "message": "Username already exists"}
        
        # Generate salt and hash password
        salt = secrets.token_hex(16)
        password_hash = self.hash_password(password, salt)
        
        # Store user with encrypted empty data
        encrypted_data = self.crypto.encrypt_data({}, password)
        
        self.users[username] = {
            "salt": salt,
            "password_hash": password_hash,
            "encrypted_data": encrypted_data
        }
        
        self.crypto.save_users(self.users)
        
        return {"success": True, "message": "Account created successfully"}
    
    def login(self, username, password):
        """Authenticate user"""
        if username not in self.users:
            return {"success": False, "message": "Invalid username or password"}
        
        user = self.users[username]
        password_hash = self.hash_password(password, user["salt"])
        
        if password_hash != user["password_hash"]:
            return {"success": False, "message": "Invalid username or password"}
        
        # Decrypt user data
        try:
            decrypted_data = self.crypto.decrypt_data(user["encrypted_data"], password)
            # Store password for this session
            self.session_passwords[username] = password
            return {"success": True, "data": decrypted_data}
        except Exception as e:
            return {"success": False, "message": "Failed to decrypt user data"}
    
    def generate_otp(self):
        """Generate 6-digit OTP for 2FA"""
        self.current_otp = str(random.randint(100000, 999999))
        return self.current_otp
    
    def verify_otp(self, otp):
        """Verify OTP code"""
        return otp == self.current_otp
    
    def update_user_data(self, username, data):
        """Update user's personal data"""
        if username not in self.users:
            return False
        
        # Get the session password for this user
        if username not in self.session_passwords:
            return False
        
        password = self.session_passwords[username]
        
        # Re-encrypt with the actual user password
        encrypted_data = self.crypto.encrypt_data(data, password)
        
        # Store encrypted data
        self.users[username]["encrypted_data"] = encrypted_data
        self.crypto.save_users(self.users)
        
        return True
    
    def logout(self, username):
        """Clear session password on logout"""
        if username in self.session_passwords:
            del self.session_passwords[username]
    
    def change_password(self, username, old_password, new_password):
        """Change user's master password"""
        # Verify old password
        login_result = self.login(username, old_password)
        if not login_result["success"]:
            return {"success": False, "message": "Invalid current password"}
        
        # Get user data
        user_data = login_result["data"]
        
        # Generate new salt and hash
        new_salt = secrets.token_hex(16)
        new_password_hash = self.hash_password(new_password, new_salt)
        
        # Re-encrypt data with new password
        encrypted_data = self.crypto.encrypt_data(user_data, new_password)
        
        # Update user record
        self.users[username] = {
            "salt": new_salt,
            "password_hash": new_password_hash,
            "encrypted_data": encrypted_data
        }
        
        self.crypto.save_users(self.users)
        
        # Update session password
        self.session_passwords[username] = new_password
        
        return {"success": True, "message": "Password changed successfully"}