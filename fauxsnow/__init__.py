import os
import asyncio
from flask import Flask, render_template
from . import weather


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'fauxsnow.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a coming soon page
    @app.route('/')
    def coming_soon():
        return render_template('coming_soon/index.html')
    
    # main page of the application
    @app.route('/main')
    def main():
        resorts = db.get_resorts()
        return render_template('main/index.html', resorts=resorts)


    @app.route('/<resort_id>/')
    def detail(resort_id):
        resort = db.get_resort_by_id(resort_id)
        return render_template('/main/detail.html', resort=resort)


    # about page of the application
    @app.route('/about')
    def about():
        return render_template('main/about.html')

    @app.route('/refresh')
    def refresh():
        db.refresh_forecasts()
        return render_template('main/refresh.html')

    return app