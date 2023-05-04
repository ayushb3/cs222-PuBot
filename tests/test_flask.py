import pytest
from flask import url_for
import pytest
from flask import Flask
import argparse
import subprocess
import time
import schedule
import wikipedia
from src.summarizer import Summarizer
from src.tweeter import Tweeter
from src.database import Database
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN


@pytest.fixture
def client():
    from webserver import app
    app.config['TESTING'] = True
    app.config['database'] = Database("test_database.db")
    app.config['tweeter'] = Tweeter(BEARER_TOKEN, API_KEY, API_SECRET,
                                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    app.config['summarizer'] = Summarizer()
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_article(client):
    response = client.get('/add_article')
    assert response.status_code == 200


def test_insert_article(client):
    data = {'author': 'John Doe', 'title': 'Test Article',
            'content': 'This is a test article.'}
    response = client.post('/articles', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Article' in response.data


def test_delete_article(client):
    response = client.post(
        '/articles/delete/John%20Doe/Test%20Article', follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Article' not in response.data

# TODO: The redirects for the update seem to cause some issue here. Not sure how to fix.

# def test_update_article(client):
#     response = client.post('/articles/update/John%20Doe/Test%20Article',
#                            data={'content': 'This is an updated article.'}, follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Test Article' in response.data
#     assert b'This is an updated article.' in response.data


def test_tweet_popup(client):
    response = client.get(
        '/articles/tweet?tweet=This%20is%20a%20test%20tweet.')
    assert response.status_code == 200
    assert b'This is a test tweet.' in response.data
