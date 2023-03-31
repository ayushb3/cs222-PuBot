# import os
# import sqlite3
# import sys

# path = os.path.abspath("src")
# sys.path.append(path)
# import database as db
from src.database import *

def test_db():
    # Create a new database
    create_table()

    # Insert a new article
    insert_article('My First Article', 'John Doe', '2022-01-01', 'This is my first article!')

    # Retrieve the content of the article
    content = get_article_content('My First Article', 'John Doe', '2022-01-01')
    assert content == 'This is my first article!'
    article = get_article('My First Article', 'John Doe', '2022-01-01')
    print(article)

    

def test_pick_article():
    have = pick_article()
    print(have)
    assert have