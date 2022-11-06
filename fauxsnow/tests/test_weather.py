import fauxsnow.weather as weather



def test_get_long_day():
    assert weather.get_long_day('2022-11-05') == 'Saturday'



def test_get_short_day():
    assert weather.get_short_day('2022-11-05') == 'S'



def test_get_weather_codes(app):
    with app.app_context():
        codes = weather.get_weather_codes()
        assert codes['1'] == 'mostly clear'



def test_get_conditions(app):
    with app.app_context():
        assert weather.get_conditions(1) == 'mostly clear'



def test_get_fs_conditions(app):
    # test day with 3 inches of snow
    assert weather.get_fs_conditions(20.3, 29.5, 20.5, '1', 1, 3.0) == 'snow'

    # test day with no snow
    assert weather.get_fs_conditions(16, 29.5, 20.5, '1', 1, 0) == 'faux'

