import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    """Create or return existing database connection"""
    if 'db' not in g:
        # Create new connection if one doesn't exist
        g.db = sqlite3.connect(
            'users.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Configure database to return rows as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database connection"""
    # Remove database connection from g object
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database using schema.sql"""
    db = get_db()
    
    # Open and execute the SQL commands from schema.sql
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def register_user(username, password):
    """Add new user to database"""
    db = get_db()
    try:
        # Insert new user with hashed password
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        # Return False if username already exists
        return False

def verify_user(username, password):
    """Verify user credentials"""
    db = get_db()
    # Find user by username
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        return None
    
    # Check if password matches
    if check_password_hash(user['password'], password):
        return user
    
    return None 

def add_project(user_id, projectname, expensetype, expenseamount, date):
    """Add new project to inventory"""
    db = get_db()
    try:
        db.execute(
            'INSERT INTO inventory (user_id, projectname, expensetype, expenseamount, date) VALUES (?, ?, ?, ?, ?)',
            (user_id, projectname, expensetype, expenseamount, date)
        )
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def get_user(user_id):
    """Get user data by ID"""
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    print(f"get_user result for id {user_id}: {user}")  # Debug print
    return user

def get_user_projects(user_id):
    """Get all projects for a user"""
    db = get_db()
    projects = db.execute(
        'SELECT * FROM projects WHERE user_id = ? ORDER BY created DESC',
        (user_id,)
    ).fetchall()
    return projects

def add_new_project(user_id, project_name):
    """Add a new project for a user"""
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO projects (user_id, name) VALUES (?, ?)',
            (user_id, project_name)
        )
        db.commit()
        return cursor.lastrowid  # Returns the ID of the new project
    except Exception as e:
        print(f"Error adding project: {e}")
        return None

def get_project_expenses(project_id):
    """Get all expenses for a project"""
    db = get_db()
    expenses = db.execute(
        'SELECT * FROM expenses WHERE project_id = ? ORDER BY date DESC',
        (project_id,)
    ).fetchall()
    return expenses

def add_expense(project_id, expense_type, amount, date):
    """Add a new expense to a project"""
    db = get_db()
    try:
        db.execute(
            'INSERT INTO expenses (project_id, expense_type, amount, date) VALUES (?, ?, ?, ?)',
            (project_id, expense_type, amount, date)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding expense: {e}")
        return False

def delete_project(project_id, user_id):
    """Delete a project and all its expenses"""
    db = get_db()
    try:
        # First verify the project belongs to the user
        project = db.execute(
            'SELECT * FROM projects WHERE id = ? AND user_id = ?',
            (project_id, user_id)
        ).fetchone()
        
        if not project:
            return False
            
        # Delete all expenses for this project
        db.execute('DELETE FROM expenses WHERE project_id = ?', (project_id,))
        # Delete the project
        db.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting project: {e}")
        return False

def delete_expense(expense_id, project_id, user_id):
    """Delete a specific expense"""
    db = get_db()
    try:
        # First verify the expense belongs to a project owned by the user
        exists = db.execute('''
            SELECT e.id FROM expenses e
            JOIN projects p ON e.project_id = p.id
            WHERE e.id = ? AND p.id = ? AND p.user_id = ?
        ''', (expense_id, project_id, user_id)).fetchone()
        
        if not exists:
            return False
            
        db.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting expense: {e}")
        return False

