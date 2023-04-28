from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')


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


@app.route('/articles', methods=['POST'])
def insert_article():
    pass


@app.route('/articles/<author>/<title>', methods=['DELETE'])
def delete_article(author, title):
    pass


@app.route('/articles/<author>/<title>', methods=['PATCH'])
def update_article(id):
    pass


@app.route('/articles/tweet/<author>/<title>', methods=['POST'])
def tweet_article(author, title):
    pass
