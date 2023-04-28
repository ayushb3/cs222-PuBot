CREATE TABLE IF NOT EXISTS articles (
    author TEXT,
    title TEXT,
    content TEXT,
    lastTweeted INTEGER DEFAULT 0,
    PRIMARY KEY (author, title)
);
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    every INTEGER DEFAULT 1,
    interval TEXT DEFAULT 'days',
    at TEXT DEFAULT NULL
);