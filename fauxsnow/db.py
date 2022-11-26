import sqlite3
from sqlite3 import Row
import pandas as pd
import click
from flask import current_app, g
import asyncio
from . import weather

def get_db():
    """
    Utility function to get connection to the database
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Utility function to close database connection
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(load_data=True):
    """
    Initialize the database by:
    1. running schema.sql to create the tables
    2. loading the resorts data from data/resorts.csv
    3. loading the forecasts data from the open-meteo API
    
    """
    db = get_db()

    # create the database tables
    click.echo('creating database tables')
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    if load_data:
        # load the resorts data
        click.echo('loading resorts')
        resorts = pd.read_csv(current_app.open_resource('data/resorts.csv'), quotechar="'")
        resorts.to_sql('resorts', get_db(), if_exists="append", index=False)

        # load the weather data
        click.echo('loading weather forecasts')
        forecasts = asyncio.run(weather.get_weather())
        save_foreacsts(forecasts)



def refresh_forecasts():
    """
    Refresh the forecast data in the db from the api
    """
    
    # get the weather forecasts
    forecasts = asyncio.run(weather.get_weather())
    print(f'API returned {len(forecasts)} forecasts.')

    if(len(forecasts) == 25):
        print('deleting forecasts')
        delete_forecasts()
        print('saving forecasts')
        save_foreacsts(forecasts)




def delete_forecasts():
    """
    Delete the forecasts from the db.
    """
    db = get_db()
    db.execute('DELETE FROM forecasts;')



def save_foreacsts(forecasts):
    """
    Save forecast data to the db.
    """

    # 
    # Forecast Periods Explained:
    #   Periods 0, 1, 2 = historic
    #   Period 3 = today
    #   Period 4, 5, 6, 7, 8, 9 = future days
    # 

    records = []
    for forecast in forecasts:

        # save the raw json to the database
        save_raw_forecast(forecast['resort_id'], forecast['current_weather']['time'], forecast)

        # load the data into a new dictionary
        record = {}
        record['resort_id'] = forecast['resort_id']
        record['forecast_time'] = forecast['current_weather']['time']
        record['sum_historic_faux_days'] = weather.get_historic(forecast)
        record['sum_forecast_snow'] = round(weather.cm_to_inch(sum(forecast['daily']['snowfall_sum'][4:10])), 1)
        record['sum_historic_snow'] = round(weather.cm_to_inch(sum(forecast['daily']['snowfall_sum'][0:3])), 1)

         # calculate the average dewpoint for each forecast period
        avg_dewpoint = weather.get_avg_value_by_date(forecast['hourly']['time'], 
                                                    forecast['hourly']['dewpoint_2m'], 
                                                    forecast['daily']['time'][3])

        record[f'today_date'] = forecast['daily']['time'][3]
        record[f'today_day_short'] = weather.get_short_day(forecast['daily']['time'][3])
        record[f'today_day_long'] = weather.get_long_day(forecast['daily']['time'][3])
        record[f'today_max_temp'] = forecast['daily']['temperature_2m_max'][3]
        record[f'today_min_temp'] = forecast['daily']['temperature_2m_min'][3]
        record[f'today_snow'] = round(weather.cm_to_inch(forecast['daily']['snowfall_sum'][3]),1)
        record[f'today_conditions'] = weather.get_conditions(forecast['daily']['weathercode'][3])
        record[f'today_fs_conditions'] = weather.get_fs_conditions(float(avg_dewpoint), 
                                                                        float(forecast['daily']['temperature_2m_max'][3]), 
                                                                        float(forecast['daily']['temperature_2m_min'][3]), 
                                                                        forecast['daily']['weathercode'][3], 
                                                                        int(forecast['resort_open']), 
                                                                        float(forecast['daily']['snowfall_sum'][3]))

        # add the forecast periods
        for i in range(4,10):
            
            # calculate the average dewpoint for each forecast period
            avg_dewpoint = weather.get_avg_value_by_date(forecast['hourly']['time'], 
                                                        forecast['hourly']['dewpoint_2m'], 
                                                        forecast['daily']['time'][i])

            record[f'fp{i-3}_date'] = forecast['daily']['time'][i]
            record[f'fp{i-3}_day_short'] = weather.get_short_day(forecast['daily']['time'][i])
            record[f'fp{i-3}_day_long'] = weather.get_long_day(forecast['daily']['time'][i])
            record[f'fp{i-3}_max_temp'] = forecast['daily']['temperature_2m_max'][i]
            record[f'fp{i-3}_min_temp'] = forecast['daily']['temperature_2m_min'][i]
            record[f'fp{i-3}_snow'] = round(weather.cm_to_inch(forecast['daily']['snowfall_sum'][i]),1)
            record[f'fp{i-3}_conditions'] = weather.get_conditions(forecast['daily']['weathercode'][i])
            record[f'fp{i-3}_fs_conditions'] = weather.get_fs_conditions(float(avg_dewpoint), 
                                                                            float(forecast['daily']['temperature_2m_max'][i]), 
                                                                            float(forecast['daily']['temperature_2m_min'][i]), 
                                                                            forecast['daily']['weathercode'][i], 
                                                                            int(forecast['resort_open']), 
                                                                            float(forecast['daily']['snowfall_sum'][i]))

        # create a dataframe from the dictionary and add it to the list of records
        forecast_record = pd.DataFrame()
        df_dictionary = pd.DataFrame(record, index=[0])
        forecast_record = pd.concat([forecast_record, df_dictionary], ignore_index=True)
        records.append(forecast_record)

    # concatenate the dataframes and save them to the database
    all_forecasts = pd.concat(records)
    all_forecasts.to_sql('forecasts', get_db(), if_exists="append", index=False)


def get_resorts() -> list:
    db = get_db()
    resorts = db.execute(
        '''
        SELECT resorts.resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, 
        main_url, conditions_url, map_url, acres, trails, lifts, vertical, resort_open, 
        forecast_time, CAST(sum_historic_faux_days as int) as sum_historic_faux_days, round(sum_forecast_snow, 1) as sum_forecast_snow, round(sum_historic_snow, 1) as sum_historic_snow,
        today_date, today_day_short, today_day_long, CAST(today_max_temp as int) as today_max_temp, CAST(today_min_temp as int) as today_min_temp, today_conditions, today_fs_conditions, round(today_snow, 1) as today_snow,
        fp1_date, fp1_day_short, fp1_day_long, CAST(fp1_max_temp as int) as fp1_max_temp, CAST(fp1_min_temp as int) as fp1_min_temp, fp1_conditions, fp1_fs_conditions, round(fp1_snow, 1) as fp1_snow,
        fp2_date, fp2_day_short, fp2_day_long, CAST(fp2_max_temp as int) as fp2_max_temp, CAST(fp2_min_temp as int) as fp2_min_temp, fp2_conditions, fp2_fs_conditions, round(fp2_snow, 1) as fp2_snow,
        fp3_date, fp3_day_short, fp3_day_long, CAST(fp3_max_temp as int) as fp3_max_temp, CAST(fp3_min_temp as int) as fp3_min_temp, fp3_conditions, fp3_fs_conditions, round(fp3_snow, 1) as fp3_snow,
        fp4_date, fp4_day_short, fp4_day_long, CAST(fp4_max_temp as int) as fp4_max_temp, CAST(fp4_min_temp as int) as fp4_min_temp, fp4_conditions, fp4_fs_conditions, round(fp4_snow, 1) as fp4_snow,
        fp5_date, fp5_day_short, fp5_day_long, CAST(fp5_max_temp as int) as fp5_max_temp, CAST(fp5_min_temp as int) as fp5_min_temp, fp5_conditions, fp5_fs_conditions, round(fp5_snow, 1) as fp5_snow,
        fp6_date, fp6_day_short, fp6_day_long, CAST(fp6_max_temp as int) as fp6_max_temp, CAST(fp6_min_temp as int) as fp6_min_temp, fp6_conditions, fp6_fs_conditions, round(fp6_snow, 1) as fp6_snow,
        fp7_date, fp7_day_short, fp7_day_long, CAST(fp7_max_temp as int) as fp7_max_temp, CAST(fp7_min_temp as int) as fp7_min_temp, fp7_conditions, fp7_fs_conditions, round(fp7_snow, 1) as fp7_snow
        FROM resorts LEFT JOIN forecasts ON resorts.resort_id = forecasts.resort_id
        '''
    ).fetchall()
    return resorts

def get_resort_by_id(resort_id:str) -> Row:
    db = get_db()
    resort = db.execute(
        '''
        SELECT resorts.resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, 
        main_url, conditions_url, map_url, acres, trails, lifts, vertical, resort_open, 
        forecast_time, sum_historic_faux_days, sum_forecast_snow, sum_historic_snow,
        today_date, today_day_short, today_day_long, CAST(today_max_temp as int) as today_max_temp, CAST(today_min_temp as int) as today_min_temp, today_conditions, today_fs_conditions, round(today_snow, 1) as today_snow,
        fp1_date, fp1_day_short, fp1_day_long, fp1_max_temp, fp1_min_temp, fp1_conditions, fp1_fs_conditions, round(fp1_snow, 1) as fp1_snow,
        fp2_date, fp2_day_short, fp2_day_long, fp2_max_temp, fp2_min_temp, fp2_conditions, fp2_fs_conditions, round(fp2_snow, 1) as fp2_snow,
        fp3_date, fp3_day_short, fp3_day_long, fp3_max_temp, fp3_min_temp, fp3_conditions, fp3_fs_conditions, round(fp3_snow, 1) as fp3_snow,
        fp4_date, fp4_day_short, fp4_day_long, fp4_max_temp, fp4_min_temp, fp4_conditions, fp4_fs_conditions, round(fp4_snow, 1) as fp4_snow,
        fp5_date, fp5_day_short, fp5_day_long, fp5_max_temp, fp5_min_temp, fp5_conditions, fp5_fs_conditions, round(fp5_snow, 1) as fp5_snow,
        fp6_date, fp6_day_short, fp6_day_long, fp6_max_temp, fp6_min_temp, fp6_conditions, fp6_fs_conditions, round(fp6_snow, 1) as fp6_snow,
        fp7_date, fp7_day_short, fp7_day_long, fp7_max_temp, fp7_min_temp, fp7_conditions, fp7_fs_conditions, round(fp7_snow, 1) as fp7_snow
        FROM resorts LEFT JOIN forecasts ON resorts.resort_id = forecasts.resort_id
        WHERE resorts.resort_id = ?
        ''',
        (resort_id,)
    ).fetchone()
    return resort

def save_raw_forecast(resort_id, forecast_time, forecast):
    db = get_db()
    db.execute(
        '''
        INSERT INTO raw_forecasts 
        (resort_id, forecast_time, forecast_data) 
        VALUES (?, ?, ?)
        ''',
    (resort_id, forecast_time, str(forecast)))
    db.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('starting databse initialization')
    init_db()
    click.echo('finished database initialization')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)