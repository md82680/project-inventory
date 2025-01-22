from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db, close_db, init_db, register_user, verify_user, add_project, get_user
from secret_key import SECRET_KEY
from datetime import timedelta

app = Flask(__name__)

# Basic configuration - this is all you need
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=30)

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
            session.clear()
            session.permanent = True
            session['user_id'] = user['id']
            print(f"Session after setting user_id: {session}")
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = get_user(session['user_id'])
    return render_template('dashboard.html', user=user, projects=[])

@app.route('/add_project', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    project_name = data.get('name')
    
    if not project_name:
        return jsonify({'success': False, 'error': 'Project name is required'})
    
    try:
        db = get_db()
        db.execute(
            'INSERT INTO projects (user_id, name) VALUES (?, ?)',
            (session['user_id'], project_name)
        )
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding project: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Initialize the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)

