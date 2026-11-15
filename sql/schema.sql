PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    owner_name TEXT NOT NULL,
    item_name TEXT NOT NULL,
    size TEXT NOT NULL,
    condition TEXT NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1
        CHECK (is_available IN (0, 1))
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS exchanges (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (requester_id) REFERENCES users(id)
);