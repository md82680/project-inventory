# Project Inventory Tracker
#### Video Demo: https://www.youtube.com/watch?v=dQw4w9WgXcQ
#### Description:

A web-based application built with Flask that helps users track project expenses. This application allows users to create multiple projects and manage their associated expenses in a simple, intuitive interface. Whether you're a contractor managing multiple job sites, a hobbyist tracking material costs, or a project manager monitoring budgets, this tool provides an organized way to track your expenses.

## Features

- User Authentication
  - Secure registration and login system
  - Password hashing using Werkzeug security
  - Session management with 30-minute timeout
  - Protection against SQL injection

- Project Management
  - Create unlimited projects
  - View all projects in an organized dropdown menu
  - Delete projects with cascade deletion of associated expenses
  - Simple and intuitive project switching

- Expense Tracking
  - Add expenses to specific projects
  - Track expense type, amount, and date
  - View comprehensive expense history for each project
  - Delete individual expenses
  - Automatic total calculation
  - Date validation and formatting

## Design Choices

Several key design decisions were made during development:

1. **Database Structure**: I chose SQLite for its simplicity and relational nature. The database is structured with three tables:
   - Users: Stores credentials with hashed passwords
   - Projects: Links projects to users
   - Expenses: Associates expenses with projects
   This structure allows for efficient querying while maintaining data integrity through foreign_idkeys.

2. **User Interface**: I opted for a minimalist design with:
   - A persistent navigation bar for easy access to key functions
   - Intuitive forms for adding projects and expenses to prevent page reloads
   - Responsive tables for expense display (add and delete)
   This ensures a smooth user experience while maintaining functionality.

3. **Security Implementation**: Security was a priority:
   - Passwords are hashed using Werkzeug
   - Session management prevents unauthorized access
   - CSRF protection through Flask's built-in features
   - Input validation on both client and server side

## File Structure and Functionality

```
ProjectInventory/
├── static/
│   ├── styles.css         # CSS styling for all pages
│   └── images/            # Static images including hero image
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # User login form
│   ├── register.html     # User registration form
│   ├── dashboard.html    # Project management interface
│   └── history.html      # Expense tracking interface
├── app.py                # Main application logic and routes
├── database.py           # Database operations and queries
├── schema.sql           # Database structure definition
└── README.md            # Project documentation
```

### Key Files Explained

- **app.py**: The core application file containing all route definitions and request handling. It manages user sessions, form processing, and coordinates between the database and templates.

- **database.py**: Handles all database operations through well-defined functions. It includes user authentication, project management, and expense tracking operations. The file uses SQLite3 with connection pooling for efficient database access.

- **schema.sql**: Defines the database structure with three main tables (users, projects, expenses). It includes foreign key constraints to maintain data integrity and proper indexing for performance.

- **templates/**: Contains Jinja2 templates for rendering pages:
  - base.html: Provides the common layout and navigation
  - dashboard.html: Main interface for project management
  - history.html: Detailed expense tracking interface
  - index.html: Landing page
  - login.html: User login form
  - register.html: User registration form

- **static/****: Contains static files for styling and images
- styles.css: CSS styling for all pages
- images/: Static images including hero image
  - hero.jpg: Hero image for the landing page

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/md82680/ProjectInventory.git
```

2. Install required packages:
```bash
pip install flask werkzeug
```

3. Generate a secret key:
```bash
python generate_key.py
  - The secret key is accessible in the app.py file.  The key is used for the session cookie.
```

4. Initialize the database:
```bash
flask init-db
```

5. Run the application:
```bash
flask run
```

## Future Improvement Considerations

- Export functionality for expense reports
- Multiple currency support
- Project categories and tags
- Budget tracking and alerts
- File attachment support for receipts
- Data visualization for expense analysis

## Credits

Created by Michael Despo for CS50x Final Project. Special thanks to the CS50 team for their excellent course material and support.
