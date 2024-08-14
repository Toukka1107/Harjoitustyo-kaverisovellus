CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    age INTEGER,
    hobbies TEXT,
    about_me TEXT
);

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    friend_id INTEGER
);

CREATE TABLE friend_requests (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER,
    receiver_id INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    subject TEXT,
    message TEXT,
    status TEXT,
    time TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    message_id INTEGER,
    comment TEXT,
    status TEXT,
    time TIMESTAMP
);
