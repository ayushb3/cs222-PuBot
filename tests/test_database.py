import os
from datetime import datetime
from src.database import Database


db = Database("test_database.db")


def test_insert():
    db.insert_article('author1', 'title1', 'content1')
    article = db.get_article('author1', 'title1')
    assert article is not None
    assert article['author'] == 'author1'
    assert article['title'] == 'title1'
    assert article['content'] == 'content1'
    assert article['lastTweeted'] == 0


def test_update_last_tweeted():
    db.insert_article('author2', 'title2', 'content2')
    db.update_last_tweeted_article('author2', 'title2')
    article = db.get_article('author2', 'title2')
    assert article is not None
    assert article['author'] == 'author2'
    assert article['title'] == 'title2'
    assert article['content'] == 'content2'
    assert article['lastTweeted'] != 0

    assert datetime.strptime(
        article['lastTweeted'], '%Y-%m-%d %H:%M:%S.%f') <= datetime.now()


def test_delete():
    db.insert_article('author3', 'title3', 'content3')
    db.delete_article('author3', 'title3')
    article = db.get_article('author3', 'title3')
    assert article is None


def test_pick():
    db.insert_article('author4', 'title4', 'content4')
    article = db.pick_article(author='author4')
    assert article is not None
    assert article['author'] == 'author4'
    assert article['title'] == 'title4'
    assert article['content'] == 'content4'
    assert article['lastTweeted'] == 0
