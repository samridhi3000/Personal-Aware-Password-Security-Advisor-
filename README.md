# 🔐 Personal-Aware Password Security Advisor (Ongoing Project)

**An enterprise-grade web application that analyzes passwords for personal information vulnerabilities and demonstrates modern cybersecurity concepts through practical implementation.**

## 🎯 Overview

Personal-Aware Password Security Advisor is a comprehensive B.Tech cybersecurity mini-project that educates users about password security by analyzing their passwords against personal information patterns. The application demonstrates how attackers exploit personal data in dictionary attacks and provides cryptographically secure password alternatives.

### Why This Project?

- **80%+ of data breaches** involve weak or compromised passwords
- **60% of users** reuse passwords across multiple sites
- **30% of passwords** contain easily guessable personal information
- This tool **educates** users about these vulnerabilities through hands-on analysis

---

## ✨ Features

### 🔍 Core Functionality

1. **Password Analyzer**
   - Detects personal information in passwords
   - Analyzes character composition
   - Calculates brute-force resistance
   - Provides detailed security reports

2. **Brute-Force Simulator**
   - Real-time crack time calculations
   - Multiple attack speed scenarios (1M/sec, 1B/sec)
   - Educational insights on password complexity

3. **Attacker Guesses Generator**
   - Demonstrates 10 most likely dictionary attack patterns
   - Shows how personal data is weaponized
   - Educational warnings about weak patterns

4. **Strong Password Generator**
   - Generates 5 cryptographically secure passwords
   - Multiple styles: Random, Passphrase, Mixed
   - Guarantees 14+ characters with full charset

5. **Personal Data Management**
   - Collects user information for analysis
   - Extracts keywords for pattern matching
   - GDPR-compliant consent management

### 🛡️ Security Features

- **End-to-End Encryption**: PBKDF2 (100,000 iterations) + Fernet (AES-128-CBC + HMAC)
- **Two-Factor Authentication**: OTP-based 2FA (sent to registered mobile)
- **Secure Sessions**: Flask session management with secret keys
- **Data Privacy**: All data stored locally with encryption
- **Input Validation**: Comprehensive form validation and sanitization

### 🎨 User Experience

- **Modern UI/UX**: Dark theme with responsive design
- **Real-time Feedback**: Instant analysis and suggestions
- **Mobile-Friendly**: Responsive across all devices
- **Interactive Dashboards**: Clean, intuitive navigation
- **Flash Notifications**: Clear user feedback

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0**: Web framework
- **Cryptography Library**: PBKDF2, Fernet encryption

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality

### Security
- **PBKDF2HMAC**: Key derivation (100k iterations)
- **Fernet**: Symmetric encryption (AES-128)
- **SHA-256**: Password hashing
- **secrets module**: Cryptographically secure random generation

### Data Storage
- **JSON**: Encrypted local storage
- **Session Management**: Flask sessions

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager


### Security Measures

- ✅ Passwords never stored in plaintext
- ✅ Salt generation using `secrets.token_hex(16)`
- ✅ Session-based authentication
- ✅ OTP expires after single use
- ✅ Input sanitization and validation
- ✅ HTTPS recommended for production


## 📁 Project Structure

```
Personal-Aware-Password-Security-Advisor/
├── app.py                      # Main Flask application
├── auth.py                     # Authentication & OTP
├── crypto_store.py             # Encryption module
├── analyzer.py                 # Password analysis engine
├── generator.py                # Password generation
├── requirements.txt            # Dependencies
├── users.json                  # Encrypted user database (auto-generated)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── login.html             # Auth page
│   ├── consent.html           # GDPR consent
│   ├── personal_data.html     # Data collection
│   ├── dashboard.html         # Main dashboard
│   ├── analyzer.html          # Password analyzer
│   ├── bruteforce.html        # Brute-force simulator
│   ├── attacker.html          # Attacker guesses
│   └── generator.html         # Password generator
│
├── static/                     # Static assets
│   ├── style.css              # Styles
│   └── script.js              # JavaScript
│
└── README.md                   # This file

## ⚠️ Disclaimer

**Educational Purpose Only**: This is an academic project for demonstrating cybersecurity concepts. While implementing industry-standard encryption, it is NOT intended for production use or storing real sensitive data. For production deployments, additional security hardening, professional security audits, and compliance certifications are required.

## 🙏 Acknowledgments

- NIST for password security guidelines
- OWASP for web security best practices
- Python cryptography library maintainers
- Flask framework contributors
- Academic advisors and mentors

**Made with ❤️ for cybersecurity education**

---

This README provides comprehensive documentation for your GitHub repository. You can customize the sections based on your specific implementation and requirements! 🚀
