"""
Password Analyzer Module
Analyzes password strength and brute-force resistance
File: analyzer.py
"""

import re
import math


class PasswordAnalyzer:
    """Analyzes passwords for strength, personal information, and brute-force resistance"""
    
    def __init__(self):
        """Initialize password analyzer with leet speak mappings"""
        self.leet_map = {
            '0': 'o', '1': 'i', '1': 'l', '3': 'e', '4': 'a',
            '5': 's', '7': 't', '8': 'b', '9': 'g', '@': 'a'
        }
    
    def normalize_leet(self, text):
        """Convert leet speak to normal text"""
        result = text.lower()
        for leet, normal in self.leet_map.items():
            result = result.replace(leet, normal)
        return result
    
    def check_personal_relation(self, password, keywords):
        """Check if password contains personal information"""
        password_lower = password.lower()
        password_normalized = self.normalize_leet(password)
        
        matched_keywords = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Direct substring match
            if keyword_lower in password_lower:
                matched_keywords.append(keyword)
                continue
            
            # Normalized (leet speak) match
            if keyword_lower in password_normalized:
                matched_keywords.append(f"{keyword} (leet speak)")
                continue
            
            # Partial match for longer keywords
            if len(keyword_lower) >= 4:
                if keyword_lower[:4] in password_lower:
                    matched_keywords.append(f"{keyword} (partial)")
        
        return matched_keywords
    
    def analyze_charset(self, password):
        """Analyze character set composition"""
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_special:
            charset_size += 32
        
        return {
            'has_lower': has_lower,
            'has_upper': has_upper,
            'has_digit': has_digit,
            'has_special': has_special,
            'charset_size': charset_size
        }
    
    def calculate_brute_force(self, password):
        """Calculate brute-force attack time estimates"""
        charset = self.analyze_charset(password)
        length = len(password)
        charset_size = charset['charset_size']
        
        if charset_size == 0:
            return None
        
        # Total combinations
        total_combinations = charset_size ** length
        
        # Time estimates at different speeds
        speeds = {
            '1 Million/sec': 1_000_000,
            '1 Billion/sec': 1_000_000_000,
        }
        
        estimates = {}
        for speed_name, guesses_per_sec in speeds.items():
            seconds = total_combinations / guesses_per_sec
            estimates[speed_name] = self.format_time(seconds)
        
        return {
            'combinations': total_combinations,
            'charset_size': charset_size,
            'length': length,
            'estimates': estimates
        }
    
    def format_time(self, seconds):
        """Format time in human-readable format"""
        if seconds < 0.001:
            return "< 1 millisecond"
        elif seconds < 1:
            return f"{seconds*1000:.2f} milliseconds"
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        elif seconds < 31536000 * 1000:
            return f"{seconds/31536000:.2f} years"
        elif seconds < 31536000 * 1000000:
            return f"{seconds/31536000/1000:.2f} thousand years"
        elif seconds < 31536000 * 1000000000:
            return f"{seconds/31536000/1000000:.2f} million years"
        else:
            return f"{seconds/31536000/1000000000:.2f} billion years"
    
    def get_strength_rating(self, password, has_personal_info):
        """Get overall strength rating"""
        length = len(password)
        charset = self.analyze_charset(password)
        
        if has_personal_info:
            return "Very Weak"
        
        if length < 8:
            return "Very Weak"
        elif length < 10:
            return "Weak"
        elif length < 12:
            if charset['charset_size'] >= 62:
                return "Moderate"
            return "Weak"
        elif length < 14:
            if charset['charset_size'] >= 62:
                return "Good"
            return "Moderate"
        else:
            if charset['charset_size'] >= 62 and charset['has_special']:
                return "Very Strong"
            elif charset['charset_size'] >= 52:
                return "Strong"
            return "Good"
    
    def analyze_password(self, password, keywords):
        """Comprehensive password analysis"""
        output = []
        output.append("═" * 80)
        output.append("PASSWORD SECURITY ANALYSIS REPORT")
        output.append("═" * 80)
        output.append("")
        
        # Basic info
        output.append(f"Password Length: {len(password)} characters")
        output.append("")
        
        # Personal information check
        output.append("─" * 80)
        output.append("PERSONAL INFORMATION DETECTION")
        output.append("─" * 80)
        
        matched = self.check_personal_relation(password, keywords)
        if matched:
            output.append("⚠️  WARNING: Password contains personal information!")
            output.append("")
            output.append("Matched Keywords:")
            for keyword in matched[:5]:
                output.append(f"  • {keyword}")
            if len(matched) > 5:
                output.append(f"  ... and {len(matched) - 5} more")
            output.append("")
            output.append("🔴 CRITICAL: Passwords based on personal information are easily")
            output.append("   guessed by attackers using dictionary attacks!")
        else:
            output.append("✓ Good: No obvious personal information detected")
        
        output.append("")
        
        # Character set analysis
        output.append("─" * 80)
        output.append("CHARACTER SET ANALYSIS")
        output.append("─" * 80)
        
        charset = self.analyze_charset(password)
        output.append(f"Lowercase letters (a-z): {'✓ Yes' if charset['has_lower'] else '✗ No'}")
        output.append(f"Uppercase letters (A-Z): {'✓ Yes' if charset['has_upper'] else '✗ No'}")
        output.append(f"Digits (0-9):            {'✓ Yes' if charset['has_digit'] else '✗ No'}")
        output.append(f"Special characters:      {'✓ Yes' if charset['has_special'] else '✗ No'}")
        output.append(f"Total charset size:      {charset['charset_size']} characters")
        output.append("")
        
        # Brute-force analysis
        output.append("─" * 80)
        output.append("BRUTE-FORCE RESISTANCE ANALYSIS")
        output.append("─" * 80)
        
        bf_data = self.calculate_brute_force(password)
        if bf_data:
            output.append(f"Search Space: {charset['charset_size']}^{len(password)} = {bf_data['combinations']:,.0f} combinations")
            output.append("")
            output.append("Time to crack at different speeds:")
            for speed, time in bf_data['estimates'].items():
                output.append(f"  • {speed:20s}: {time}")
        output.append("")
        
        # Strength rating
        strength = self.get_strength_rating(password, bool(matched))
        output.append("─" * 80)
        output.append("OVERALL STRENGTH RATING")
        output.append("─" * 80)
        
        rating_colors = {
            "Very Weak": "🔴",
            "Weak": "🟠",
            "Moderate": "🟡",
            "Good": "🟢",
            "Strong": "🟢",
            "Very Strong": "🟢"
        }
        
        output.append(f"{rating_colors.get(strength, '⚪')} {strength}")
        output.append("")
        
        # Recommendations
        output.append("─" * 80)
        output.append("RECOMMENDATIONS")
        output.append("─" * 80)
        
        issues = []
        suggestions = []
        
        if matched:
            issues.append("Contains personal information")
            suggestions.append("Use completely random characters unrelated to your life")
        
        if len(password) < 14:
            issues.append(f"Password is too short ({len(password)} chars)")
            suggestions.append("Use at least 14 characters for strong security")
        
        if not charset['has_upper']:
            issues.append("No uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
        
        if not charset['has_digit']:
            issues.append("No digits")
            suggestions.append("Add numbers (0-9)")
        
        if not charset['has_special']:
            issues.append("No special characters")
            suggestions.append("Add special characters (!@#$%^&*)")
        
        if issues:
            output.append("Issues Found:")
            for issue in issues:
                output.append(f"  ✗ {issue}")
            output.append("")
            output.append("Suggestions:")
            for suggestion in suggestions:
                output.append(f"  → {suggestion}")
        else:
            output.append("✓ No major issues found! This is a strong password.")
        
        output.append("")
        output.append("═" * 80)
        
        return "\n".join(output)
    
    def brute_force_simulation(self):
        """Generate brute-force simulation explanation"""
        output = []
        output.append("═" * 80)
        output.append("BRUTE-FORCE ATTACK SIMULATION")
        output.append("═" * 80)
        output.append("")
        
        output.append("A brute-force attack tries every possible password combination until")
        output.append("it finds the correct one. The time required depends on:")
        output.append("")
        output.append("1. CHARACTER SET SIZE (N)")
        output.append("   • Lowercase only (a-z): 26 characters")
        output.append("   • + Uppercase (A-Z): 52 characters")
        output.append("   • + Digits (0-9): 62 characters")
        output.append("   • + Special (!@#$%): ~94 characters")
        output.append("")
        output.append("2. PASSWORD LENGTH (L)")
        output.append("   Total combinations = N^L")
        output.append("")
        output.append("3. ATTACKER SPEED (guesses per second)")
        output.append("   • Consumer GPU: ~1 million/sec")
        output.append("   • Supercomputer/Botnet: ~1 billion/sec")
        output.append("")
        
        output.append("─" * 80)
        output.append("EXAMPLE CALCULATIONS")
        output.append("─" * 80)
        output.append("")
        
        examples = [
            ("lowercase only", 8, 26),
            ("lowercase + digits", 8, 36),
            ("mixed case + digits", 10, 62),
            ("all character types", 14, 94),
        ]
        
        for desc, length, charset in examples:
            combinations = charset ** length
            time_slow = combinations / 1_000_000
            time_fast = combinations / 1_000_000_000
            
            output.append(f"Password: {length} chars, {desc}")
            output.append(f"  Combinations: {combinations:,.0f}")
            output.append(f"  Time @ 1M/sec: {self.format_time(time_slow)}")
            output.append(f"  Time @ 1B/sec: {self.format_time(time_fast)}")
            output.append("")
        
        output.append("─" * 80)
        output.append("KEY INSIGHTS")
        output.append("─" * 80)
        output.append("")
        output.append("✓ Adding just ONE character multiplies the search space by charset size")
        output.append("✓ A 14-character password with all char types = 1.4 x 10^27 combinations")
        output.append("✓ Even at 1 billion guesses/sec, this would take millions of years")
        output.append("")
        output.append("⚠️  However, attackers DON'T use pure brute-force!")
        output.append("   They use DICTIONARY ATTACKS that try common patterns first:")
        output.append("   • Personal information (names, dates)")
        output.append("   • Common words + numbers (password123)")
        output.append("   • Simple patterns (qwerty, 123456)")
        output.append("")
        output.append("This is why avoiding personal information is CRITICAL!")
        output.append("")
        output.append("═" * 80)
        
        return "\n".join(output)