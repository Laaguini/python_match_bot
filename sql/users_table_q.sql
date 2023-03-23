CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL, 
    name TEXT, 
    age INTEGER, 
    preferred_age_min INTEGER, 
    preferred_age_max INTEGER, 
    gender TEXT, 
    preferred_gender TEXT,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS user_pictures (
    user_id INTEGER NOT NULL,
    telegram_file_id INTEGER, 
    src INTEGER
);

CREATE TABLE IF NOT EXISTS user_replies (
    from_id INTEGER NOT NULL,
    to_id INTEGER NOT NULL, 
    message TEXT
);