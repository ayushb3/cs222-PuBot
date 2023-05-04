from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, static_url_path='/static')


@app.template_global()
def _len(item):
    return len(item)


@app.route('/')
def index():
    return render_template(
        'index.html',
        schedule=app.config['database'].get_schedule(),
        articles=app.config['database'].get_articles()
    )


@app.route('/start', methods=['POST'])
def start_scheduler():
    pass


@app.route('/stop', methods=['POST'])
def stop_scheduler():
    pass


@app.route('/scheduler', methods=['PATCH'])
def update_scheduler():
    app.config['database'].upsert_schedule(
        every=int(request.form['every']),
        interval=request.form['interval'],
        at=request.form['at']
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
    article_content = app.config['database'].get_article(author, title)[2]
    app.config['summarizer'].make_tweet(article_content)
    tweet = app.config['summarizer'].get_content()[:280]

    app.config['tweeter'].tweet(tweet)

    return render_template('tweet.html', tweet=tweet)


@app.route('/articles/tweet', methods=['GET'])
def tweet_popup():
    tweet = request.args.get('tweet', '')

    return render_template('tweet.html', tweet=tweet)
