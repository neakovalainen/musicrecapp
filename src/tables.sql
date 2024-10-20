CREATE TABLE Users (
    id  SERIAL PRIMARY KEY, 
    username  TEXT UNIQUE,
    password  TEXT,
);

CREATE TABLE Posts (
  id  SERIAL PRIMARY KEY,
  content TEXT,
  user_id  INTEGER,
  creation_time  TIMESTAMP DEFAULT NOW(),

  FOREIGN KEY (user_id) REFERENCES Users(id)
    ON DELETE CASCADE
);

CREATE TABLE Friends (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  friend_id INTEGER,

  FOREIGN KEY (user_id) REFERENCES Users(id)
    ON DELETE CASCADE,
  FOREIGN KEY (friend_id) REFERENCES Users(id)
    ON DELETE CASCADE
);

CREATE TABLE Likes (
  id  SERIAL PRIMARY KEY,
  post_id  INTEGER,
  liker_id  INTEGER,

  FOREIGN KEY (post_id) REFERENCES Posts(id)
    ON DELETE CASCADE,
  FOREIGN KEY (liker_id) REFERENCES Users(id)
    ON DELETE CASCADE,

  UNIQUE (post_id, liker_id)
);

CREATE TABLE Bios (
  id  SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE,
  bio TEXT,

  FOREIGN KEY (user_id) REFERENCES Users(id)
);