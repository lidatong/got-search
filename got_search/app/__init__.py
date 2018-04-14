from typing import Type
from got_search.app.config import Config
from flask import Flask, render_template
from got_search.app.seasons import seasons as seasons_blueprint
from got_search.app.episodes import episodes as episodes_blueprint


def create_app(config: Type[Config]):
    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)

    app.register_blueprint(seasons_blueprint)
    app.register_blueprint(episodes_blueprint)

    return app
