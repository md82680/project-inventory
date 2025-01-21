CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    projectname TEXT NOT NULL,
    expensetype TEXT NOT NULL,
    expenseamount REAL NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
); 