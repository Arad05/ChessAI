-- 1. Create the 'users' table.
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,         -- Store hashed password in a real system.
    nickname VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    country VARCHAR(50),
    rating INTEGER DEFAULT 1200,              -- Default rating per User class.
    role VARCHAR(20) DEFAULT 'user',
    online_status BOOLEAN DEFAULT FALSE,      -- Online/offline status.
    ban_end TIMESTAMPTZ,                      -- Ban expiration; NULL means not banned.
    join_date TIMESTAMPTZ DEFAULT NOW()       -- Join date is set at creation.
);


-- 2. Create the 'games' table.
CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    opponent VARCHAR(100),
    opponent_nickname VARCHAR(50),
    result VARCHAR(10),                       -- Expected values: 'win', 'loss', 'draw'
    game_date TIMESTAMPTZ                     -- Date and time when the game was played.
);

-- 3. Create the 'user_friends' table.
-- This table represents a bidirectional friendship.
CREATE TABLE user_friends (
    user_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    friend_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    PRIMARY KEY (user_email, friend_email)
);


CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    sender_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    receiver_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    message_content JSONB NOT NULL,  -- JSON field to store message data
    sent_at TIMESTAMPTZ DEFAULT NOW()  -- Timestamp of when the message was sent
);
