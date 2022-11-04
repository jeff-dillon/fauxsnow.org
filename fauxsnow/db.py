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
        '''
        SELECT resorts.resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, 
        main_url, conditions_url, map_url, acres, trails, lifts, vertical, 
        forecast_time, sum_historic_faux_days, sum_forecast_snow, 
        fp1_date, fp1_day_short, fp1_day_long, fp1_max_temp, fp1_min_temp, fp1_avg_hum, fp1_weathercode, fp1_conditions, fp1_fs_conditions,
        fp2_date, fp2_day_short, fp2_day_long, fp2_max_temp, fp2_min_temp, fp2_avg_hum, fp2_weathercode, fp2_conditions, fp2_fs_conditions,
        fp3_date, fp3_day_short, fp3_day_long, fp3_max_temp, fp3_min_temp, fp3_avg_hum, fp3_weathercode, fp3_conditions, fp3_fs_conditions,
        fp4_date, fp4_day_short, fp4_day_long, fp4_max_temp, fp4_min_temp, fp4_avg_hum, fp4_weathercode, fp4_conditions, fp4_fs_conditions,
        fp5_date, fp5_day_short, fp5_day_long, fp5_max_temp, fp5_min_temp, fp5_avg_hum, fp5_weathercode, fp5_conditions, fp5_fs_conditions,
        fp6_date, fp6_day_short, fp6_day_long, fp6_max_temp, fp6_min_temp, fp6_avg_hum, fp6_weathercode, fp6_conditions, fp6_fs_conditions,
        fp7_date, fp7_day_short, fp7_day_long, fp7_max_temp, fp7_min_temp, fp7_avg_hum, fp7_weathercode, fp7_conditions, fp7_fs_conditions
        FROM resorts LEFT JOIN forecasts ON resorts.resort_id = forecasts.resort_id
        '''
    ).fetchall()
    return resorts

def get_resort_by_id(resort_id:str) -> Row:
    db = get_db()
    resort = db.execute(
        '''
        SELECT resorts.resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, 
        main_url, conditions_url, map_url, acres, trails, lifts, vertical, 
        forecast_time, sum_historic_faux_days, sum_forecast_snow, 
        fp1_date, fp1_day_short, fp1_day_long, fp1_max_temp, fp1_min_temp, fp1_avg_hum, fp1_weathercode, fp1_conditions, fp1_fs_conditions,
        fp2_date, fp2_day_short, fp2_day_long, fp2_max_temp, fp2_min_temp, fp2_avg_hum, fp2_weathercode, fp2_conditions, fp2_fs_conditions,
        fp3_date, fp3_day_short, fp3_day_long, fp3_max_temp, fp3_min_temp, fp3_avg_hum, fp3_weathercode, fp3_conditions, fp3_fs_conditions,
        fp4_date, fp4_day_short, fp4_day_long, fp4_max_temp, fp4_min_temp, fp4_avg_hum, fp4_weathercode, fp4_conditions, fp4_fs_conditions,
        fp5_date, fp5_day_short, fp5_day_long, fp5_max_temp, fp5_min_temp, fp5_avg_hum, fp5_weathercode, fp5_conditions, fp5_fs_conditions,
        fp6_date, fp6_day_short, fp6_day_long, fp6_max_temp, fp6_min_temp, fp6_avg_hum, fp6_weathercode, fp6_conditions, fp6_fs_conditions,
        fp7_date, fp7_day_short, fp7_day_long, fp7_max_temp, fp7_min_temp, fp7_avg_hum, fp7_weathercode, fp7_conditions, fp7_fs_conditions
        FROM resorts LEFT JOIN forecasts ON resorts.resort_id = forecasts.resort_id
        WHERE resorts.resort_id = ?
        ''',
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