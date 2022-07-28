-- Users Table
CREATE TABLE users (
    id serial PRIMARY KEY,
    username text NOT NULL UNIQUE,
    email text NOT NULL UNIQUE,
    hashed_password text NOT NULL
);

-- Sentences Table

CREATE TABLE sentences (
    id serial PRIMARY KEY,
    user_id integer NOT NULL,
    sentence text NOT NULL,
    likes integer DEFAULT 0,
    liked_by_users integer[] DEFAULT array[]::integer[]
);

--column in sentences called - liked_by_users integer[]
-- example: get all sentences liked by user_id 5

SELECT * 
FROM sentences
WHERE 5 = ANY (liked_users);
