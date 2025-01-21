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