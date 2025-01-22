import flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db, close_db, init_db, register_user, verify_user
from werkzeug.security import generate_password_hash, check_password_hash
from secret_key import SECRET_KEY
app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = verify_user(username, password)
        if user is not None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

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
    # Add dashboard logic here
    return render_template('dashboard.html')

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Initialize the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)