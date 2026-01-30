"""
Password Generator Module
Generates strong passwords and educational attacker guesses
File: generator.py
"""

import secrets
import string
import random


class PasswordGenerator:
    """Generates secure passwords and demonstrates weak password patterns"""
    
    def __init__(self):
        """Initialize password generator with word list"""
        self.wordlist = [
            'correct', 'horse', 'battery', 'staple', 'purple', 'monkey',
            'dishwasher', 'elephant', 'piano', 'rainbow', 'bicycle', 
            'mountain', 'ocean', 'tiger', 'dragon', 'phoenix', 'crystal',
            'thunder', 'silver', 'golden', 'emerald', 'diamond', 'marble'
        ]
    
    def generate_strong_passwords(self, keywords_to_avoid):
        """Generate 5 cryptographically secure passwords"""
        output = []
        output.append("═" * 80)
        output.append("STRONG PASSWORD RECOMMENDATIONS")
        output.append("═" * 80)
        output.append("")
        output.append("These passwords are:")
        output.append("✓ Cryptographically secure (using secrets module)")
        output.append("✓ At least 14 characters long")
        output.append("✓ Mix of lowercase, uppercase, digits, and special characters")
        output.append("✓ NO personal information included")
        output.append("")
        output.append("─" * 80)
        output.append("")
        
        passwords = []
        
        # Generate 5 different types of passwords
        for i in range(5):
            if i < 2:
                password = self.generate_random_password(16)
            elif i < 4:
                password = self.generate_passphrase()
            else:
                password = self.generate_mixed_pattern()
            
            # Ensure no personal keywords
            if not self.contains_keywords(password, keywords_to_avoid):
                passwords.append(password)
        
        for i, pwd in enumerate(passwords, 1):
            output.append(f"Password {i}:")
            output.append(f"  {pwd}")
            output.append(f"  Length: {len(pwd)} characters")
            output.append("")
        
        output.append("─" * 80)
        output.append("HOW TO USE THESE PASSWORDS")
        output.append("─" * 80)
        output.append("")
        output.append("1. Choose one password you can remember (or use a password manager)")
        output.append("2. Write it down ONLY in a secure place (NOT on your device)")
        output.append("3. Practice typing it several times")
        output.append("4. NEVER share it with anyone")
        output.append("5. Use different passwords for different accounts")
        output.append("")
        output.append("💡 TIP: Passphrase-style passwords (like Password 3-4) are often")
        output.append("   easier to remember while still being very secure!")
        output.append("")
        output.append("═" * 80)
        
        return "\n".join(output)
    
    def generate_random_password(self, length=16):
        """Generate pure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Ensure it has all character types
        while not (any(c.islower() for c in password) and
                  any(c.isupper() for c in password) and
                  any(c.isdigit() for c in password) and
                  any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)):
            password = ''.join(secrets.choice(chars) for _ in range(length))
        
        return password
    
    def generate_passphrase(self):
        """Generate passphrase-style password"""
        words = random.sample(self.wordlist, 3)
        numbers = ''.join(str(secrets.randbelow(10)) for _ in range(2))
        special = secrets.choice("!@#$%^&*")
        
        # Capitalize words
        words = [w.capitalize() for w in words]
        
        # Combine in pattern
        password = f"{words[0]}{words[1]}{numbers}{special}{words[2]}"
        
        return password
    
    def generate_mixed_pattern(self):
        """Generate mixed pattern password"""
        word = secrets.choice(self.wordlist).capitalize()
        numbers = ''.join(str(secrets.randbelow(10)) for _ in range(3))
        special1 = secrets.choice("!@#$%^&*")
        special2 = secrets.choice("!@#$%^&*")
        suffix = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(2))
        
        password = f"{special1}{word}{numbers}{special2}{suffix}"
        
        return password
    
    def contains_keywords(self, password, keywords):
        """Check if password contains any keywords"""
        password_lower = password.lower()
        for keyword in keywords:
            if keyword.lower() in password_lower:
                return True
        return False
    
    def generate_attacker_guesses(self, keywords, user_data):
        """Generate educational examples of weak passwords"""
        output = []
        output.append("═" * 80)
        output.append("ATTACKER'S DICTIONARY - EDUCATIONAL DEMONSTRATION")
        output.append("═" * 80)
        output.append("")
        output.append("⚠️  CRITICAL WARNING ⚠️")
        output.append("")
        output.append("These passwords demonstrate WEAK patterns that attackers try FIRST")
        output.append("in dictionary attacks. NEVER use passwords like these!")
        output.append("")
        output.append("Attackers build custom dictionaries using:")
        output.append("  • Your name and variations")
        output.append("  • Your date of birth")
        output.append("  • Phone numbers")
        output.append("  • Social media handles")
        output.append("  • Common substitutions (a→@, e→3, i→1)")
        output.append("")
        output.append("─" * 80)
        output.append("TOP 10 GUESSES AN ATTACKER WOULD TRY:")
        output.append("─" * 80)
        output.append("")
        
        # Extract useful data
        name_parts = user_data.get("full_name", "John Doe").lower().split()
        first_name = name_parts[0] if name_parts else "john"
        last_name = name_parts[-1] if len(name_parts) > 1 else "doe"
        nickname = user_data.get("nickname", first_name).lower()
        
        dob = user_data.get("dob", "01/01/2000")
        dob_parts = dob.split("/")
        if len(dob_parts) == 3:
            day, month, year = dob_parts
            short_year = year[-2:]
        else:
            day, month, year, short_year = "01", "01", "2000", "00"
        
        phone = user_data.get("phone", "1234567890")
        phone_digits = ''.join(c for c in phone if c.isdigit())
        
        instagram = user_data.get("instagram", "").replace("@", "").lower()
        
        # Generate 10 weak password patterns
        patterns = [
            (f"{first_name}123", "name + sequential numbers"),
            (f"{first_name}{year}", "name + birth year"),
            (f"{nickname}@{short_year}", "leet speak substitution"),
            (f"{day}{month}{year}", "date of birth only"),
            (phone_digits[-10:] if len(phone_digits) >= 10 else "1234567890", "phone number"),
            (f"{first_name}_{last_name}{short_year}", "name combination"),
            (instagram if instagram else f"{first_name}_insta", "social media handle"),
            (f"{first_name.capitalize()}{day}{month}", "name + date combination"),
            (f"{nickname}{year}", "nickname + year"),
            (f"{last_name}{day}{month}", "last name + date")
        ]
        
        for i, (guess, explanation) in enumerate(patterns, 1):
            output.append(f"{i:2d}. {guess:30s} ← {explanation}")
        
        output.append("")
        output.append("─" * 80)
        output.append("WHY THESE ARE DANGEROUS")
        output.append("─" * 80)
        output.append("")
        output.append("Modern password cracking tools:")
        output.append("  • Can try millions of guesses per second")
        output.append("  • Use leaked password databases to learn patterns")
        output.append("  • Automatically generate variations of personal info")
        output.append("  • Try common substitutions (@ for a, 3 for e, etc.)")
        output.append("")
        output.append(f"A password like '{first_name}{year}' might seem unique to you, but:")
        output.append("  • It's in the first 100 guesses an attacker would try")
        output.append("  • Could be cracked in under 1 second")
        output.append("  • Appears in millions of leaked password databases")
        output.append("")
        output.append("─" * 80)
        output.append("WHAT TO DO INSTEAD")
        output.append("─" * 80)
        output.append("")
        output.append("✓ Use completely random characters (see Strong Password Generator)")
        output.append("✓ Make it at least 14 characters long")
        output.append("✓ Avoid ANY personal information")
        output.append("✓ Use a password manager to remember complex passwords")
        output.append("✓ Enable two-factor authentication (2FA) on all accounts")
        output.append("")
        output.append("Remember: If you can easily remember it, an attacker can easily")
        output.append("guess it. Strong passwords should be random and unique!")
        output.append("")
        output.append("═" * 80)
        
        return "\n".join(output)