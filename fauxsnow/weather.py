import asyncio
import aiohttp
import datetime
import yaml
import pandas as pd
from flask import current_app, g
from urllib import parse
from . import db


url = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=dewpoint_2m&daily=weathercode,temperature_2m_max,temperature_2m_min,snowfall_sum&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&past_days=3&resort_id={}&resort_open={}'

def get_tasks(session:aiohttp.ClientSession, resorts:list) -> list:
    """
    Utility function used in async API calls.
    """
    tasks = []
    for resort in resorts:
        tasks.append(session.get(url.format(resort['lat'], resort['lon'], resort['resort_id'], resort['resort_open']), ssl=True))

    return tasks

async def get_weather() -> list:
    """
    Calls the open-meteo.com weather api for each resort and returns a list of dictionaries with the weather forecasts.
    """
    forecasts = []
    resorts = db.get_resorts()
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, resorts)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            forecast = await response.json()

            # retrive the resort_id and resort_open values from the url
            this_url = str(response.url)
            params = dict(parse.parse_qsl(parse.urlsplit(this_url).query))
            forecast['resort_id'] = params['resort_id']
            forecast['resort_open'] = params['resort_open']

            forecasts.append(forecast)

    return forecasts


# TODO implement
def get_historic():
    return 3



def get_short_day(date_str: str) -> str:
    """
    Formats a date string (YYYY-MM-DD) into a Weekday name abbreviated (i.e 'M')
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%a')[0]



def get_long_day(date_str: str) -> str:
    """
    Formats a date string (YYYY-MM-DD) into a full Weekday name (i.e. 'Monday')
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')



def get_avg_value_by_date(dates: list, values: list, selected_date: str) -> float:
    """
    Calculates the average values given a list of values.
    """
   # combine the lists into a dataframe
    df = pd.DataFrame(zip(dates, values), columns=['date','values'])

    # slice the date string to ignore the time portion
    df['date'] = df['date'].apply(lambda x : x[0:10])

    # calculate the average by date
    means = df.groupby('date').mean().reset_index()

    # get the average for the selected date
    avg_value = str(round(means.loc[means['date'] == selected_date, 'values'], 1).iloc[0])
    return avg_value



def get_weather_codes() -> dict:
    """
    Returns a dictinoary of weather code : conditions literal pairs.
    """
    if 'weather_codes' not in g:
        with current_app.open_resource('data/weather_codes.yaml') as f:
            g.weather_codes = yaml.load(f, Loader=yaml.FullLoader)
    return g.weather_codes



def get_conditions(code: int) -> str:
    """
    Returns the weather conditions literal given a code
    """
    weather_codes = get_weather_codes()
    return weather_codes[str(code)]



def get_fs_conditions(dewpoint: float, max_temp: float, min_temp: float, weathercode: str, resort_open: int, snowfall_sum: float) -> str:
    """
    calculates one of four possible conditions
    1. nothing (-) : default - conditions don't match the other three options
    2. snow : weathercode in [71, 73, 75, 77, 85, 86] or snowfall sum < .05 inches
    3. faux : wet bulb temperature 20F or below and resort is open
    4. icy : weathercode in [56, 57, 66, 67] or temperature above 32F resort is open
    """

    # snowmaking conditions require a wet bulb temperature of 20F or below
    #
    # A quick technique that many forecasters use to determine the wet-bulb 
    # temperature is called the "1/3 rule". The technique is to first find the 
    # dewpoint depression (temperature minus dewpoint). Then take this number 
    # and divide by 3. Subtract this number from the temperature. You now have 
    # an approximation for the wet-bulb temperature.
    # source: https://theweatherprediction.com/habyhints/170
    #
    # Formula:
    # dewpoint_depression = temp - dewpoint 
    # delta = dewpoint_depression / 3
    # wet_bulb = temperature - delta

    # return values
    FAUX = 'faux'
    ICY = 'icy'
    SNOW = 'snow'
    NOTHING = '-'

    # weather codes
    snow_codes = [71, 73, 75, 77, 85, 86]
    icy_codes = [56, 57, 66, 67]
    rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]

    # calculate the wet bulb temperature based on the max temperature
    max_dewpoint_depression = max_temp - dewpoint
    max_delta = max_dewpoint_depression / 3
    max_wbt = max_temp - max_delta

    # calculate the wet bulb temperature based on the min temperature
    min_dewpoint_depression = min_temp - dewpoint
    min_delta = min_dewpoint_depression / 3
    min_wbt = min_temp - min_delta

    if(min_wbt <= 20 or max_wbt <= 20 and resort_open):
        return FAUX

    if(weathercode in snow_codes or snowfall_sum >= 0.5):
        return SNOW

    if((weathercode in icy_codes or weathercode in rain_codes) and resort_open):
        return ICY

    return NOTHING