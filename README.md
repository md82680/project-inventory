# Project Inventory Tracker
#### Video Demo: <https://www.youtube.com/watch?v=RsOEJ9CUOJc>
#### Description:

A web-based application built with Flask that helps users track project expenses. This application allows users to create multiple projects and manage their associated expenses in a simple, intuitive interface.

## Features

- User Authentication
  - Secure registration and login system
  - Password hashing for security
  - Session management

- Project Management
  - Create new projects
  - View all projects in a dropdown menu
  - Delete projects (cascading delete with associated expenses)

- Expense Tracking
  - Add expenses to specific projects
  - Track expense type, amount, and date
  - View expense history for each project
  - Delete individual expenses
  - Automatic total calculation

## Technologies Used

- Backend: Python with Flask framework
- Database: SQLite3
- Frontend: HTML, CSS, JavaScript
- Security: Werkzeug security for password hashing

## Database Structure

The application uses three main tables:
- Users: Stores user credentials
- Projects: Stores project information linked to users
- Expenses: Stores expense details linked to projects

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ProjectInventory.git
```

2. Install required packages:
```bash
pip install flask
```

3. Set up the database:
```bash
flask init-db
```

4. Run the application:
```bash
flask run
```

## Usage

1. Register a new account or login
2. Create a new project from the dashboard
3. Select a project to view/add expenses
4. Add expenses with type, amount, and date
5. View expense history and totals
6. Delete expenses or entire projects as needed

## File Structure

```
ProjectInventory/
├── static/
│   ├── styles.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── history.html
├── app.py
├── database.py
├── schema.sql
└── README.md
```

## Security Features

- Password hashing using Werkzeug
- Session management
- User authentication for all protected routes
- Input validation and sanitization

## Credits

Created by Micheael Despo for CS50x Final Project
