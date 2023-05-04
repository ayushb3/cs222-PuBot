from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from src.commands import _tweet_scheduler, _tweet

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)


@app.template_global()
def _len(item):
    return len(item)


@app.route('/')
def index():
    return render_template(
        'index.html',
        scheduler=app.config['database'].get_schedule(),
        articles=app.config['database'].get_articles(),
        scheduler_running=app.config['scheduler'] is not None
    )


def emit_tweet(tweet):
    with app.test_request_context('/'):
        socketio.emit('tweet', tweet['id'])


@app.route('/start', methods=['POST'])
def start_scheduler():
    if app.config['scheduler'] is None:
        schedule = app.config['database'].get_schedule()
        app.config['scheduler'] = _tweet_scheduler(
            app.config['database'].filepath,
            app.config['summarizer'],
            app.config['tweeter'],
            schedule['every'],
            schedule['interval'],
            schedule['at'],
            emit_tweet
        )
    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop_scheduler():
    if app.config['scheduler'] is not None:
        app.config['scheduler'].set()
        app.config['scheduler'] = None
    return redirect(url_for('index'))


@app.route('/scheduler', methods=['POST'])
def update_scheduler():
    app.config['database'].upsert_schedule(
        every=int(request.form['every']),
        interval=request.form['interval'],
        at=request.form.get('at', None)
    )
    return redirect(url_for('index'))


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        return redirect(url_for('insert_article'))
    else:
        return render_template('insert_article.html')


@app.route('/articles', methods=['POST'])
def insert_article():
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')

    app.config['database'].insert_article(author, title, content)

    return redirect(url_for('index'))


@app.route('/articles/delete/<author>/<title>', methods=['POST'])
def delete_article(author, title):
    app.config['database'].delete_article(author, title)
    return redirect(url_for('index'))


@app.route('/articles/update/<author>/<title>', methods=['GET', 'POST'])
def update_article(author, title):
    article = app.config['database'].get_article(author, title)
    if request.method == 'POST':
        content = request.form['content']
        app.config['database'].update_article(author, title, content)
        return redirect(url_for('index'))
    return render_template('update.html', article=article)


@app.route('/articles/tweet/<author>/<title>', methods=['POST'])
def tweet_article(author, title):
    # article_content = app.config['database'].get_article(author, title)[2]
    # app.config['summarizer'].make_tweet(article_content)
    # tweet = app.config['summarizer'].get_content()[:280]
    # app.config['tweeter'].tweet(tweet)
    article = app.config['database'].get_article(author, title)
    tweet = _tweet(article, app.config['summarizer'], app.config['tweeter'])
    return render_template('tweet.html', status_id=tweet['id'])


@app.route('/articles/tweet', methods=['GET'])
def tweet_popup():
    tweet = request.args.get('tweet', '')
    return render_template('tweet.html', tweet=tweet)
