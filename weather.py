from opencage.geocoder import OpenCageGeocode
import requests

key = 'ea0bf2d504184284aea00c654a7d223c'
geocoder = OpenCageGeocode(key)
dark_sky_key = '3791825728010421348fcd82f5fe793f'


def get_weather_data(weather_parameters):
    city = weather_parameters['queryResult']['parameters']['geo-city']
    date = weather_parameters['queryResult']['parameters']['date']
    date_period = weather_parameters['queryResult']['parameters']['date-period']
    coordinates = get_city_coordinates(city)

    parameters = {'units': 'ca'}

    weather_data = requests.get('https://api.darksky.net/forecast/' + dark_sky_key + '/' + coordinates[0] + ','
                                + coordinates[1], params=parameters)

    weather_data_dictionary = weather_data.json()

    hourly_weather_data = parse_hourly_weather_data(weather_data_dictionary)

    print(hourly_weather_data)


def get_city_coordinates(city):
    result = geocoder.geocode(city)
    if result and len(result):
        longitude = str(result[0]['geometry']['lng'])
        latitude = str(result[0]['geometry']['lat'])

    return [latitude, longitude]


def parse_hourly_weather_data(weather_data):
    hourly_weather_data = weather_data['hourly']['data']

    hourly_temperatures = []
    hourly_wind_speed = []

    for data in hourly_weather_data:
        hourly_temperatures.append(data['temperature'])
        hourly_wind_speed.append(data['windSpeed'])

    return [hourly_temperatures, hourly_wind_speed]
