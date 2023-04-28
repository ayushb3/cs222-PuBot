import sqlite3
import datetime


class Database:
    def __init__(self, filepath):
        self.filepath = filepath
        # ? may not be safe to use check_same_thread=False
        self.db = sqlite3.connect(filepath, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        with open('src/sql/schema.sql', 'r') as sql_file:
            self.db.executescript(sql_file.read())
        # Add default schedule
        self.db.execute('''INSERT OR IGNORE INTO schedules (id) VALUES (0)''')
        self.db.commit()

    def insert_article(self, author: str, title: str, content: str) -> None:
        self.db.execute('''INSERT OR REPLACE INTO articles
                            (author, title, content)
                            VALUES (?, ?, ?)''', (author, title, content))
        self.db.commit()

    def update_article(self, author: str, title: str, content: str) -> None:
        self.db.execute('''UPDATE articles
                            SET content = ?
                        WHERE author = ? AND title = ?''', (content, author, title))
        self.db.commit()


    def get_article(self, author: str, title: str) -> sqlite3.Row:
        cursor = self.db.execute('''SELECT * FROM articles
                                    WHERE author = ? AND title = ?''',
                                 (author, title))
        return cursor.fetchone()

    def get_articles(self) -> list[sqlite3.Row]:
        cursor = self.db.execute('''SELECT * FROM articles''')
        return cursor.fetchall()

    def update_last_tweeted_article(self, author: str, title: str, last_tweeted: int = None) -> None:
        if last_tweeted is None:
            last_tweeted = datetime.datetime.now()
        self.db.execute('''UPDATE articles
                        set lastTweeted = ?
                        WHERE author = ? AND title = ?''',
                        (last_tweeted, author, title))
        self.db.commit()

    def delete_article(self, author: str, title: str) -> None:
        self.db.execute('''DELETE FROM articles
                           WHERE author = ? AND title = ?''',
                        (author, title))
        self.db.commit()

    def pick_article(self, last_tweeted: str = None, author: str = None) -> sqlite3.Row:
        query = '''SELECT * FROM articles WHERE 1=1 '''
        params = ()
        if last_tweeted is not None:
            query += '''AND lastTweeted < ? '''
            params += (last_tweeted,)
        if author is not None:
            query += '''AND author = ? '''
            params += (author,)
        query += "ORDER BY random() LIMIT 1"
        cursor = self.db.execute(query, params)
        return cursor.fetchone()

    def upsert_schedule(self, every: int, interval: str, at: str = None, pk=0) -> None:
        self.db.execute('''INSERT OR REPLACE INTO schedules
                            (id, every, interval, at)
                            VALUES (?, ?, ?, ?)''',
                        (pk, every, interval, at))
        self.db.commit()

    def get_schedule(self, pk=0) -> sqlite3.Row:
        cursor = self.db.execute('''SELECT * FROM schedules
                                    WHERE id = ?''', (pk,))
        return cursor.fetchone()

    def delete_schedule(self, pk) -> None:
        if pk == 0:
            raise ValueError("Cannot delete default schedule")
        self.db.execute('''DELETE FROM schedules
                            WHERE id = ?''', (pk,))
        self.db.commit()
