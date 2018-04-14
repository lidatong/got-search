from flask import render_template
from got_search.app import create_app
from got_search.app.config import Config
from got_search.app.episodes import render_season_and_episodes

app = create_app(Config)


@app.route('/')
def index():
    return render_season_and_episodes('Game of Thrones')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
