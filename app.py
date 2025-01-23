from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import (
    get_db, 
    close_db, 
    init_db, 
    register_user, 
    verify_user, 
    add_project, 
    get_user,
    get_user_projects,
    add_new_project,
    get_project_expenses,
    add_expense,
    delete_project,
    delete_expense
)
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
    projects = get_user_projects(session['user_id'])
    return render_template('dashboard.html', user=user, projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    project_name = data.get('name')
    
    if not project_name:
        return jsonify({'success': False, 'error': 'Project name is required'})
    
    project_id = add_new_project(session['user_id'], project_name)
    if project_id:
        return jsonify({'success': True, 'project_id': project_id})
    return jsonify({'success': False, 'error': 'Failed to add project'})

@app.route('/project/<int:project_id>')
def project_history(project_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Verify the project belongs to the user
    db = get_db()
    project = db.execute(
        'SELECT * FROM projects WHERE id = ? AND user_id = ?',
        (project_id, session['user_id'])
    ).fetchone()
    
    if not project:
        flash('Project not found')
        return redirect(url_for('dashboard'))
    
    expenses = get_project_expenses(project_id)
    return render_template('history.html', project=project, expenses=expenses)

@app.route('/project/<int:project_id>/add_expense', methods=['POST'])
def add_project_expense(project_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    # Verify the project belongs to the user
    db = get_db()
    project = db.execute(
        'SELECT * FROM projects WHERE id = ? AND user_id = ?',
        (project_id, session['user_id'])
    ).fetchone()
    
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'})
    
    data = request.get_json()
    if not all(key in data for key in ['type', 'amount', 'date']):
        return jsonify({'success': False, 'error': 'Missing required fields'})
    
    success = add_expense(
        project_id=project_id,
        expense_type=data['type'],
        amount=data['amount'],
        date=data['date']
    )
    
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to add expense'})

@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project_route(project_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    if delete_project(project_id, session['user_id']):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to delete project'})

@app.route('/project/<int:project_id>/expense/<int:expense_id>/delete', methods=['POST'])
def delete_expense_route(project_id, expense_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    if delete_expense(expense_id, project_id, session['user_id']):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to delete expense'})

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Initialize the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)

