DROP TABLE IF EXISTS weather;

CREATE TABLE weather(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_accessed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  longitude FLOAT NOT NULL,
  latitude FLOAT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL,
  icon TEXT NOT NULL,
  temperature FLOAT NOT NULL,
  condition TEXT NOT NULL
);
