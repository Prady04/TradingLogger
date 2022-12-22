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
    price INTEGER,
    profit INTEGER,
    FOREIGN KEY (phonenumber) REFERENCES users (phonenumber)
);

CREATE TABLE "patterns" (
	"pattern_id"	INTEGER NOT NULL,
	"stock"	TEXT NOT NULL,
	"pattern"	TEXT NOT NULL,
	"date"	TEXT NOT NULL,
	PRIMARY KEY("pattern_id" AUTOINCREMENT)
);