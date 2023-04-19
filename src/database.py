import sqlite3
import datetime


class Database:
    def __init__(self, filepath):
        self.filepath = filepath
        self.db = sqlite3.connect(filepath)
        self.db.row_factory = sqlite3.Row
        self.db.execute('''CREATE TABLE IF NOT EXISTS articles (
                            author TEXT,
                            title TEXT,
                            content TEXT,
                            lastTweeted INTEGER DEFAULT 0,
                            PRIMARY KEY (author, title)
                        );''')
        self.db.commit()

    def insert(self, author: str, title: str, content: str) -> None:
        self.db.execute('''INSERT OR REPLACE INTO articles
                            (author, title, content)
                            VALUES (?, ?, ?)''', (author, title, content))
        self.db.commit()

    def get(self, author: str, title: str) -> tuple:
        cursor = self.db.execute('''SELECT * FROM articles
                                    WHERE author = ? AND title = ?''',
                                 (author, title))
        return cursor.fetchone()

    def update_last_tweeted(self, author: str, title: str, last_tweeted: int = None) -> None:
        if last_tweeted is None:
            last_tweeted = datetime.datetime.now()
        self.db.execute('''UPDATE articles
                        set lastTweeted = ?
                        WHERE author = ? AND title = ?''',
                        last_tweeted, author, title)
        self.db.commit()

    def delete(self, author: str, title: str) -> None:
        self.db.execute('''DELETE FROM articles
                           WHERE author = ? AND title = ?''',
                        (author, title))
        self.db.commit()

    def pick(self, last_tweeted: str = None, author: str = None) -> tuple:
        query = '''SELECT * FROM articles WHERE 1=1 '''
        params = ()
        if last_tweeted is not None:
            query += '''AND lastTweeted < ? '''
            params += last_tweeted
        if author is not None:
            query += '''AND author = ? '''
            params += author
        query += "ORDER BY random() LIMIT 1"
        self.db.execute(query, params)
        return self.db.fetchone()
