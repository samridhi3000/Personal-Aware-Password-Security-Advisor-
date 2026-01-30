"""
Personal-Aware Password Security Advisor - Web Version
Main Flask Application
File: app.py
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
import secrets
import random

from auth import AuthManager
from crypto_store import CryptoStore
from analyzer import PasswordAnalyzer
from generator import PasswordGenerator

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # For session management
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize managers
crypto = CryptoStore()
auth = AuthManager(crypto)
analyzer = PasswordAnalyzer()
generator = PasswordGenerator()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Consent required decorator
def consent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_data' not in session or not session.get('user_data', {}).get('consent_given'):
            flash('Please provide consent and personal data', 'error')
            return redirect(url_for('consent'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please fill all fields', 'error')
            return render_template('login.html')
        
        result = auth.login(username, password)
        
        if result['success']:
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            session['pending_otp'] = otp
            session['pending_username'] = username
            session['pending_data'] = result['data']
            
            flash(f'Your OTP Code: {otp} (Demo: This would be sent to your device)', 'info')
            return render_template('login.html', show_otp=True)
        else:
            flash(result['message'], 'error')
    
    return render_template('login.html')


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    """Verify OTP"""
    otp = request.form.get('otp', '')
    
    if otp == session.get('pending_otp'):
        session['username'] = session.pop('pending_username')
        session['user_data'] = session.pop('pending_data')
        session.pop('pending_otp', None)
        
        # Check if consent given
        if session['user_data'].get('consent_given'):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('consent'))
    else:
        flash('Invalid OTP', 'error')
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not password:
            flash('Please fill all fields', 'error')
            return render_template('login.html')
        
        if len(password) < 8:
            flash('Master password must be at least 8 characters', 'error')
            return render_template('login.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('login.html')
        
        result = auth.signup(username, password)
        
        if result['success']:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
    
    return render_template('login.html')


@app.route('/consent', methods=['GET', 'POST'])
@login_required
def consent():
    """GDPR consent page"""
    if request.method == 'POST':
        consent1 = request.form.get('consent1')
        consent2 = request.form.get('consent2')
        consent3 = request.form.get('consent3')
        consent4 = request.form.get('consent4')
        
        if all([consent1, consent2, consent3, consent4]):
            return redirect(url_for('personal_data'))
        else:
            flash('You must accept all terms to continue', 'error')
    
    return render_template('consent.html')


@app.route('/personal_data', methods=['GET', 'POST'])
@login_required
def personal_data():
    """Personal data collection page"""
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name', '').strip(),
            'nickname': request.form.get('nickname', '').strip(),
            'dob': request.form.get('dob', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'email': request.form.get('email', '').strip(),
            'instagram': request.form.get('instagram', '').strip(),
            'twitter': request.form.get('twitter', '').strip(),
            'facebook': request.form.get('facebook', '').strip(),
            'college': request.form.get('college', '').strip(),
            'city': request.form.get('city', '').strip(),
            'fav_word1': request.form.get('fav_word1', '').strip(),
            'fav_word2': request.form.get('fav_word2', '').strip(),
            'fav_word3': request.form.get('fav_word3', '').strip(),
            'consent_given': True
        }
        
        # Validate required fields
        required = ['full_name', 'dob', 'phone', 'email']
        if not all(data.get(field) for field in required):
            flash('Please fill all required fields', 'error')
            return render_template('personal_data.html', data=data)
        
        # Save data
        session['user_data'] = data
        auth.update_user_data(session['username'], data)
        
        flash('Personal data saved securely!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('personal_data.html')


@app.route('/dashboard')
@login_required
@consent_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', username=session['username'])


@app.route('/analyzer', methods=['GET', 'POST'])
@login_required
@consent_required
def analyze():
    """Password analyzer"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if not password:
            return jsonify({'error': 'Please enter a password'})
        
        # Extract keywords from user data
        user_data = session.get('user_data', {})
        keywords = extract_keywords(user_data)
        
        # Analyze password
        result = analyzer.analyze_password(password, keywords)
        
        return jsonify({'result': result})
    
    return render_template('analyzer.html')


@app.route('/bruteforce')
@login_required
@consent_required
def bruteforce():
    """Brute-force simulator"""
    simulation = analyzer.brute_force_simulation()
    return render_template('bruteforce.html', simulation=simulation)


@app.route('/attacker')
@login_required
@consent_required
def attacker():
    """Attacker guesses"""
    user_data = session.get('user_data', {})
    keywords = extract_keywords(user_data)
    guesses = generator.generate_attacker_guesses(keywords, user_data)
    return render_template('attacker.html', guesses=guesses)


@app.route('/generator', methods=['GET', 'POST'])
@login_required
@consent_required
def generate_passwords():
    """Strong password generator"""
    user_data = session.get('user_data', {})
    keywords = extract_keywords(user_data)
    passwords = generator.generate_strong_passwords(keywords)
    return render_template('generator.html', passwords=passwords)


@app.route('/personal_info')
@login_required
@consent_required
def personal_info():
    """View personal data"""
    user_data = session.get('user_data', {})
    return jsonify(user_data)


@app.route('/logout')
def logout():
    """Logout"""
    username = session.get('username')
    if username:
        auth.logout(username)
    
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


def extract_keywords(user_data):
    """Extract keywords from personal data"""
    import re
    
    keywords = []
    
    # Extract from name
    if user_data.get('full_name'):
        name_parts = user_data['full_name'].lower().split()
        keywords.extend(name_parts)
    
    if user_data.get('nickname'):
        keywords.append(user_data['nickname'].lower())
    
    # Extract from DOB
    if user_data.get('dob'):
        dob = user_data['dob']
        parts = dob.split('/')
        if len(parts) == 3:
            day, month, year = parts
            keywords.extend([day, month, year, day+month, month+year, 
                           day+month+year, year[-2:]])
    
    # Extract from phone
    if user_data.get('phone'):
        phone = re.sub(r'\D', '', user_data['phone'])
        keywords.append(phone)
        if len(phone) >= 4:
            keywords.append(phone[-4:])
            keywords.append(phone[:4])
    
    # Extract from social media
    for field in ['instagram', 'twitter', 'facebook']:
        if user_data.get(field):
            handle = user_data[field].replace('@', '').lower()
            keywords.append(handle)
    
    # Extract from other fields
    for field in ['college', 'city', 'fav_word1', 'fav_word2', 'fav_word3']:
        if user_data.get(field):
            keywords.append(user_data[field].lower())
    
    # Remove duplicates
    keywords = list(set([k for k in keywords if k]))
    
    return keywords


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)