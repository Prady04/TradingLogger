CREATE TABLE users (
    phonenumber INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT
);

CREATE TABLE entries (
    entry_id INTEGER PRIMARY KEY,
    phonenumber INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    transactiontype TEXT NOT NULL,
    quantity INTEGER NOT NULL,
        
    notes TEXT,
    SL INTEGER,
    FOREIGN KEY (phonenumber) REFERENCES users (phonenumber)
);