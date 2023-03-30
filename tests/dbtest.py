import os
import sqlite3
import sys

path = os.path.abspath("src")
sys.path.append(path)
import database as db


# Create a new database
db.create_table()

# Insert a new article
db.insert_article('My First Article', 'John Doe', '2022-01-01', 'This is my first article!')

# Retrieve the content of the article
content = db.get_article_content('My First Article', 'John Doe', '2022-01-01')
print(content)
article = db.get_article('My First Article', 'John Doe', '2022-01-01')
print(article)