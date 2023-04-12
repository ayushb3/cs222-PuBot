import os
import sqlite3
import sys
import datetime

path = os.path.abspath("src")
sys.path.append(path)
import database as db


# Create a new database
db.create_table()

# Insert a new article
today = datetime.date.today()
print(today)
db.insert_article('My First Article', 'John Doe', str(today), '2022-01-01','This is my first article!')

# Retrieve the content of the article

article = db.get_single_article('My First Article', 'John Doe')
print((article))
content = db.get_single_article_content('My First Article', 'John Doe')
print(content)