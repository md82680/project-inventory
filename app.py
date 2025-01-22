import flask
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db, close_db, init_db, register_user, verify_user, add_project, get_user
from secret_key import SECRET_KEY
from datetime import timedelta

app = Flask(__name__)

# Basic session configuration
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=30)

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
        
        print(f"Login attempt for user: {username}")
        user = verify_user(username, password)
        print(f"User verification result: {user}")
        
        if user is not None:
            print(f"Session before clear: {session}")
            session.clear()
            session.permanent = True
            session['user_id'] = user['id']
            print(f"Session after setting user_id: {session}")
            
            # Try to immediately verify the session was set
            print(f"Immediate session check: {session.get('user_id')}")
            
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password. Please register if you don\'t have an account.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
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
    print(f"Dashboard - Current session: {session}")
    print(f"Dashboard - user_id in session: {session.get('user_id')}")
    
    if 'user_id' not in session:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('login'))
    
    user = get_user(session['user_id'])
    print(f"Dashboard - User data: {user}")
    
    if user is None:
        session.clear()
        return redirect(url_for('login'))
        
    return render_template('dashboard.html', user=user, projects=[])

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

