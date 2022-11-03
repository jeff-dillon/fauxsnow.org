import sqlite3
from sqlite3 import Row
import pandas as pd
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(load_data=True):
    db = get_db()

    # create the database tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    if load_data:
        # load the resorts data
        resorts = pd.read_csv(current_app.open_resource('data/resorts.csv'), quotechar="'")
        resorts.to_sql('resorts', get_db(), if_exists="append", index=False)

def get_resorts() -> list:
    db = get_db()
    resorts = db.execute(
        'SELECT resort_id, resort_name, logo_file_name, '
        'state_full, state_short, address_full, lat, lon, '
        'main_url, conditions_url, map_url, '
        'acres, trails, lifts, vertical '
        'FROM resorts'
    ).fetchall()
    return resorts

def get_resort_by_id(resort_id:str) -> Row:
    db = get_db()
    resort = db.execute(
        'SELECT resort_id, resort_name, logo_file_name, '
        'state_full, state_short, address_full, lat, lon, '
        'main_url, conditions_url, map_url, '
        'acres, trails, lifts, vertical '
        'FROM resorts '
        'WHERE resort_id = ?',
        (resort_id,)
    ).fetchone()
    return resort

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)