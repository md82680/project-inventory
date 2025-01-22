import flask
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db, close_db, init_db, register_user, verify_user, add_project, get_user
from secret_key import SECRET_KEY
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

@app.before_request
def clear_session_on_startup():
    if not app.debug:
        session.clear()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = verify_user(username, password)
        print(f"User verification result: {user}")  # Debug print
        
        if user is not None:
            session.clear()
            session['user_id'] = user['id']
            print(f"Session after login: {session}")  # Debug print
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if register_user(username, password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    print(f"Current session: {session}")  # Debug print
    
    if 'user_id' not in session:
        print("No user_id in session, redirecting to login")  # Debug print
        return redirect(url_for('login'))
    
    # Get user data
    user = get_user(session['user_id'])
    print(f"User data: {user}")  # Debug print
    
    # Get user's projects (we'll implement this later)
    projects = []  # This will be populated with actual projects later
    
    if user is None:
        print("User not found in database")  # Debug print
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=user, projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    result = add_project(
        session['user_id'],
        data['projectname'],
        data['expensetype'],
        data['expenseamount'],
        data['date']
    )
    
    if result:
        return jsonify({'success': True})
    return jsonify({'error': 'Failed to add project'}), 400

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Initialize the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)

